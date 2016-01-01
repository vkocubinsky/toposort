#!/usr/bin/env python3
import unittest

from toposort import *


# Right Topologies a,b,c
# no lines: a = a, b = b, c = c
# 2 line: a < b, c = c
# 3 line: a < b < c
# split : a < (b,c)
# join : (a,b) < c   
 
# Cycles
# 1 line cycle: a < a, b = b, c = c
# 2 line cycle: a < b < a, c = c
# 3 line cycle: a < b < c < a

# => CURSOR

# Mix
# Join and cycle either: (a,b) < c, c < a, c < b
# Join and cycle one: (a,b) < c, c < a
# Split and cycle either: a < (b,c), b < a, c < a 
# Split and cycle one: a < (b,c), b < a
# Duplicate: a < b , a < b
# Transitive Duplicate: a < b, b < c, a < c


# Dictionary
# edge 
# vertex, vertices, nodes  
# transitivity, reflectivity, antisymmetry
# class Node, class edge
# a < b, a == a, {a < b, a == a, c > a, a < b < c}
# See Python condition

a = 'a'
b = 'b'
c = 'c'
abc = ['a','b','c']

class TestABC(unittest.TestCase):

    def assertSort(self, edges, unordered, ordered):
        self.assertCountEqual(unordered, ordered)
        self.assertOrder(edges, ordered)

    def assertOrder(self, edges, ordered):
        for edge in edges:
            before, after = edge
            with self.subTest(edge='{} < {}'.format(*edge)):
                if edge[0] != edge[1]:
                    self.assertOrderLess(*edge,ordered)

    def assertOrderLess(self, a, b, ordered):
        self.assertTrue(ordered.index(a) < ordered.index(b)) 

    def test_no_lines(self):
        """ No lines: a = a, b = b, c = c"""
        edges = [(a,a), (b,b), (c,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_2_nodes_line(self):
        """ 2 nodes line: a < b, c = c """
        edges = [(a,b),(c,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_3_nodes_line(self):
        """ 3 nodes line: a < b < c """
        edges = [(a,b),(b,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_split(self):
        """ Split : a < b, a < c """
        edges = [(a,b),(a,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_join(self):
        """ Join : a < c, b < c """  
        edges = [(a,c),(b,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_2_nodes_cycle(self):
        """ 2 nodes line cycle: a < b < a, c = c """
        edges = [(a,b),(b,a),(c,c)]
        with self.assertRaises(CycleException):
            sort_edges(edges)

    def test_3_nodes_cycle(self):
        """ 3 nodes line cycle: a < b < c < a """
        edges = [(a,b),(b,c),(c,a)]
        with self.assertRaises(CycleException):
            sort_edges(edges)

if __name__ == '__main__':
    unittest.main()
