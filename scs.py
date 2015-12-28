#! /usr/bin/env python
from __future__ import print_function
import unittest

""" SHORTEST COMMON SUPERSTRING
Find a shortest (possibly non-unique) superstring that contains all the given substrings
For example: ["suit","case","it"] -> "suitcase" (and also "casesuit")
             ["suit","case","it","suitcase"] -> "suitcase" (now unique)
"""

import collections
import heapq

Partition = collections.namedtuple('Partition', 'prefix sufix')

class Heap(object):
    """A min-heap."""

    def __init__(self):
        self._values = []

    def push(self, value):
        """Push the value item onto the heap."""
        heapq.heappush(self._values, value)

    def pop(self):
        """ Pop and return the smallest item from the heap."""
        return heapq.heappop(self._values)

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        yield from self._values

class ProtoSuperstringCollection(collections.defaultdict):

    def __init__(self,*args,**kwargs):

        self._keys = Heap()
        super().__init__(*args,**kwargs)

    def __setitem__(self, key, value):
        if key not in self._keys:
            self._keys.push(key)

        super().__setitem__(key,value)

    def popmin(self):

        return self._keys.pop()


def generate_partitions(word):

    for i in reversed(range(len(word)+1)):
        yield Partition(prefix=word[:i],sufix=word[i:])


def minSuperstring(wordList):
    """
    Generate the shortest superstring that contains all the given substrings
    :param wordList: List of all the substrings - List of str
    :return: String representing the superstring - Str
    """

    # We will use Dykstra algorithm to do this thing. The strategy is to glue the substrings together until we have no
    # more substrings to glue. The problem is that a given substring could be in our proto-superstring so when we
    # "glue" substring together we have to "trim" the common parts.

    proto_superstrings = ProtoSuperstringCollection(set)

    # Start with the empty string

    proto_superstrings[0].add("")

    while True:

        # Iterate thought the  minimum set of superstrings

        min_len = proto_superstrings.popmin()

        while proto_superstrings[min_len]:

            prefix = proto_superstrings[min_len].pop()

            added_new_word = False # Initialize the the flag for new additions

            for word in wordList:

                # if the word is already in our prefix, skip the word.
                if word in prefix:
                    continue

                added_new_word = True # We have added at least one word

                # Generate new possible proto_superstrings using the prefix and the wordList
                for partition in generate_partitions(word):
                    if prefix.endswith(partition.prefix):
                        new_superstring = prefix + partition.sufix
                        proto_superstrings[len(new_superstring)].add(new_superstring)

            # If we reach the max_len then yield all the superstrings

            if not added_new_word:
                return prefix

        # As we have used all proto_superstrings, delete the dict item for that
        del proto_superstrings[min_len]

def minSuperstringCheck(self,wordList, length):
    minSuper=minSuperstring(wordList)
    self.assertEqual (len(minSuper),length) # Check with a test-provided length
    for w in wordList:
        self.assertTrue(w in minSuper) # Check substrings

class minSuperstringTest(unittest.TestCase):

    def test1(self):
        minSuperstringCheck(self,["suit","case","it"],8)
        minSuperstringCheck(self,["suit","case","it",""],8)
    def test2(self):
        minSuperstringCheck(self,["suit","case","it","suitcase"],8)
        minSuperstringCheck(self,["case","suit","it","suitcase"],8)
        minSuperstringCheck(self,["suitcase","case","suit","it"],8)
        minSuperstringCheck(self,["suitcase","casesuit"],12)
    def test3(self):
        minSuperstringCheck(self,["AGATTA","GATTACA","TACAGA"],10)
    def test4(self):
        minSuperstringCheck(self,["CCCTG","TGACA","CATGA"],11)
    def test5(self):
        minSuperstringCheck(self,['LOREM', 'DOLOR', 'SED', 'DO', 'MAGNA', 'AD', 'DOLORE'],14)
    def testNP(self):
        # The problem is NP-complete. You can check the increase in complexity with this test
        lLen=6
        l=list(map(chr, range(97, 97+lLen))) #["a","b",...]
        minSuperstringCheck(self,l,lLen)


if __name__ == "__main__":
    unittest.main()
