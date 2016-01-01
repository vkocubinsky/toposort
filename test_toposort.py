#!/usr/bin/env python3
import unittest
from toposort import *

# Symbols
a = 'a'
b = 'b'
c = 'c'
abc = ['a','b','c']

class TestManualSortABC(unittest.TestCase):

    def assertCycle(self, edges):
        with self.assertRaises(CycleException):
            sort_edges(edges)

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
        """No lines: a = a, b = b, c = c"""
        edges = [(a,a), (b,b), (c,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_2_nodes_line(self):
        """2 nodes line: a < b, c = c"""
        edges = [(a,b),(c,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_3_nodes_line(self):
        """3 nodes line: a < b < c"""
        edges = [(a,b),(b,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_split(self):
        """Split: a < b, a < c"""
        edges = [(a,b),(a,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_join(self):
        """Join : a < c, b < c"""  
        edges = [(a,c),(b,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges, abc, ordered)

    def test_2_nodes_cycle(self):
        """2 nodes line cycle: a < b < a, c = c"""
        edges = [(a,b),(b,a),(c,c)]
        with self.assertRaises(CycleException):
            sort_edges(edges)

    def test_3_nodes_cycle(self):
        """3 nodes line cycle: a < b < c < a"""
        edges = [(a,b),(b,c),(c,a)]
        self.assertCycle(edges)

    def test_join_and_cycle_either(self):
        """Join and cycle either: a < c, b < c, c < a, c < b"""
        edges = [(a,c),(b,c),(c,a),(c,b)]
        self.assertCycle(edges)

    def test_join_and_cycle_one(self):
        """Join and cycle either: a < c, b < c, c < a"""
        edges = [(a,c),(b,c),(c,a)]
        self.assertCycle(edges)

    def test_split_and_cycle_either(self):
        """Split and cycle either: a < b, a < c, b < a, c < a"""
        edges = [(a,b),(a,c),(b,a),(c,a)]
        self.assertCycle(edges)

    def test_split_and_cycle_one(self):
        """Split and cycle one: a < b, a < c, b < a"""
        edges = [(a,b),(a,c),(b,a)]
        self.assertCycle(edges)

    def test_duplicate(self):
        """Duplicate: a < b , a < b, c = c"""
        edges = [(a,b),(a,b),(c,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges,abc,ordered)

    def test_transitive(self):
        """Transitive: a < b, b < c, a < c"""
        edges = [(a,b),(b,c),(a,c)]
        ordered = sort_edges(edges)
        self.assertSort(edges,abc,ordered)


if __name__ == '__main__':
    unittest.main()
