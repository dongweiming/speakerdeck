"""Port forwarder with graceful exit.

Run the example as

  python portforwarder.py :8080 gevent.org:80

Then direct your browser to http://localhost:8080 or do "telnet localhost 8080".

When the portforwarder receives TERM or INT signal (type Ctrl-C),
it closes the listening socket and waits for all existing
connections to finish. The existing connections will remain unaffected.
The program will exit once the last connection has been closed.

Modify from https://github.com/surfly/gevent/blob/master/examples/portforwarder.py
"""
import sys
import signal
import gevent
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname


class PortForwarder(StreamServer):

    def __init__(self, listener, dest, **kwargs):
        StreamServer.__init__(self, listener, **kwargs)
        self.dest = dest

    def handle(self, source, address):
        if address[:2][0] != 'xxx': # 如果不是公司的外网ip 就不要理了
            return
        log('%s:%s accepted', *address[:2])
        try:
            dest = create_connection(self.dest)
        except IOError, ex:
            log('%s:%s failed to connect to %s:%s: %s', address[0], address[1], self.dest[0], self.dest[1], ex)
            return
        gevent.spawn(forward, source, dest)
        gevent.spawn(forward, dest, source)

    def close(self):
        if self.closed:
            sys.exit('Multiple exit signals received - aborting.')
        else:
            log('Closing listener socket')
            StreamServer.close(self)


def forward(source, dest):
    try:
        while True:
            try:
                data = source.recv(1024)
            except:
                break
            if not data:
                break
            dest.sendall(data)
    finally:
        source.close()
        dest.close()


def parse_address(address):
    try:
        hostname, port = address.rsplit(':', 1)
        port = int(port)
    except ValueError:
        sys.exit('Expected HOST:PORT: %r' % address)
    return gethostbyname(hostname), port


def pf_for_qq(*args):

    dest = parse_address('{0}:{1}'.format(args[0], args[1]))
    source = '0.0.0.0:{0}'.format(args[2])
    server = PortForwarder(source, dest)
    log('Starting port forwarder %s:%s -> %s:%s', *(server.address[:2] + dest))
    gevent.signal(signal.SIGTERM, server.close)
    gevent.signal(signal.SIGINT, server.close)
    server.start()
    gevent.wait()

def main():
    args = sys.argv[1]
    dest = parse_address('xxx.xxx.xxx.%s:port' % args)
    if len(args) == 2:
	args = '0%s' % args
    source = '0.0.0.0:59%s' % args
    #source = args[0]
    #dest = parse_address(args[1])
    server = PortForwarder(source, dest)
    log('Starting port forwarder %s:%s -> %s:%s', *(server.address[:2] + dest))
    gevent.signal(signal.SIGTERM, server.close)
    gevent.signal(signal.SIGINT, server.close)
    server.start()
    gevent.wait()

def log(message, *args):
    message = message % args
    sys.stderr.write(message + '\n')


if __name__ == '__main__':
    main()
