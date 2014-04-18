#!/usr/bin/env python
# Author: Dongweiming
'''
http://code.admaster.co/snippets/26
http://pymotw.com/2/multiprocessing/mapreduce.html
'''
import glob
import collections
import itertools
import operator
import multiprocessing


class AdMapReduce(object):

    def __init__(self, map_func, reduce_func, num_workers=None):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)

    def partition(self, mapped_values):
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()

    def run(self, inputs, chunksize=1):
        map_responses = self.pool.map(self.map_func, inputs,
                                      chunksize=chunksize)
        partitioned_data = self.partition(itertools.chain(*map_responses))
        reduced_values = self.pool.map(self.reduce_func, partitioned_data)
        return reduced_values


def mapper(one_line):
    l = one_line.strip().split()
    return [(word, 1) for word in l]


def reducer(item):
    word, occurances = item
    return (word, sum(occurances))


if __name__ == '__main__':
    with open('ecstasy.txt') as f:
        inputs = f.readlines()
    mp = AdMapReduce(mapper, reducer)
    result = mp.run(inputs)
    print sorted(result, key=operator.itemgetter(1), reverse=True)
