#coding=utf-8

import sys
import multiprocessing
sys.path.append('/home/dongwm/.local/lib64/python2.6/site-packages/gevent-1.0dev-py2.6-linux-x86_64.egg')
sys.path.append('/home/dongwm/.local/lib64/python2.6/site-packages/greenlet-0.4.0-py2.6-linux-x86_64.egg/')

from portforwarder import pf_for_qq

if __name__ == "__main__":
    #import pdb;pdb.set_trace()
    l = [
        ('123.126.84.158', 5902, 60037),
        ('123.126.84.159', 5902, 60038),
        ('123.126.84.160', 5902, 60039),
        ('123.126.84.161', 5902, 60040),
        # qq mongodb环境
        #('192.168.1.100', 27017, 60040),
        # qq mysql
        #('192.168.1.100', 3306, 60047),
        # sina mysql
        #('192.168.1.82', 3306, 60048),
        # sina mongodb环境
        #('192.168.1.104', 27017, 60041),
        #('192.168.1.90', 27017, 60042),
        #('192.168.1.90', 27019, 60043),
        #('192.168.1.90', 27018, 60049),
        #('192.168.1.90', 27020, 60050),
        #('192.168.1.197', 27017, 60045),
        #('192.168.1.196', 27017, 60046),
        #('192.168.1.106', 27017, 60044)
       ]
    jc = []
    try:
        for catch in l:
            m = multiprocessing.Process(target=pf_for_qq, args=catch)
            m.daemon = True
            m.start()
            jc.append(m)

        for i in jc:
            m.join()
    except KeyboardInterrupt:
        for i in jc:
            i.terminate()
