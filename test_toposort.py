#!/usr/bin/env python3
import unittest
from toposort import *

# Symbols
a = 'a'
b = 'b'
c = 'c'

class ToposortTestCase(unittest.TestCase):

    def distinct_nodes(self,edges):
        nodes = set()
        for edge in edges:
            nodes.add(edge[0])
            nodes.add(edge[1])
        return nodes    


    def assertCycle(self, edges, cycle=None):
        with self.assertRaises(CycleException) as e:
            list(sort_edges(edges))
        if cycle: 
            self.assertEqual(cycle, e.exception.cycle)    

    def assertSort(self, edges_iter):
        edges_list = list(edges_iter)
        allnodes = self.distinct_nodes(edges_list)
        for edges in (list(edges_list),iter(edges_list)):
            with self.subTest(edges_type = str(type(edges))):
                sorted_iter = sort_edges(edges)
                sorted_list = list(sorted_iter)
                self.assertCountEqual(sorted_list, allnodes)
                self.assertOrder(edges, sorted_list)

    def assertOrder(self, edges, ordered):
        for edge in edges:
            before, after = edge
            with self.subTest(edge='{} < {}'.format(*edge)):
                if edge[0] != edge[1]:
                    self.assertOrderLess(*edge,ordered)

    def assertOrderLess(self, a, b, ordered):
        self.assertTrue(ordered.index(a) < ordered.index(b)) 


class ZeroNodesTestCase(ToposortTestCase):

    def testZero(self):
        self.assertSort([])
   

class TwoNodesTestCase(ToposortTestCase):
    
    def testTwo(self):
        for n1 in (a,None,False,True): 
            for n2 in (a,None,False,True): 
                edges = [(n1,n2)]
                with self.subTest(edges=edges):
                    self.assertSort(edges)

class ThreeNodesTestCase(ToposortTestCase):


    def test_no_lines(self):
        """a = a, b = b, c = c"""
        edges = [(a,a), (b,b), (c,c)]
        self.assertSort(edges)

    def test_2_nodes_line(self):
        """a < b, c = c"""
        edges = [(a,b),(c,c)]
        self.assertSort(edges)

    def test_3_nodes_line(self):
        """a < b < c"""
        edges = [(a,b),(b,c)]
        self.assertSort(edges)

    def test_split(self):
        """a < b, a < c"""
        edges = [(a,b),(a,c)]
        self.assertSort(edges)

    def test_join(self):
        """a < c, b < c"""  
        edges = [(a,c),(b,c)]
        self.assertSort(edges)

    def test_2_nodes_cycle(self):
        """a < b < a, c = c"""
        edges = [(a,b),(b,a),(c,c)]
        self.assertCycle(edges, [a,b])

    def test_3_nodes_cycle(self):
        """a < b < c < a"""
        edges = [(a,b),(b,c),(c,a)]
        self.assertCycle(edges,[a,b,c])

    def test_join_and_cycle_either(self):
        """a < c, b < c, c < a, c < b"""
        edges = [(a,c),(b,c),(c,a),(c,b)]
        self.assertCycle(edges, [a,c]) # there are 2 cycle

    def test_join_and_cycle_one(self):
        """a < c, b < c, c < a"""
        edges = [(a,c),(b,c),(c,a)]
        self.assertCycle(edges,[a,c])

    def test_split_and_cycle_either(self):
        """a < b, a < c, b < a, c < a"""
        edges = [(a,b),(a,c),(b,a),(c,a)]
        self.assertCycle(edges, [a,b]) # there are 2 cycle

    def test_split_and_cycle_one(self):
        """a < b, a < c, b < a"""
        edges = [(a,b),(a,c),(b,a)]
        self.assertCycle(edges, [a,b])

    def test_duplicate(self):
        """a < b , a < b, c = c"""
        edges = [(a,b),(a,b),(c,c)]
        self.assertSort(edges)

    def test_transitive(self):
        """a < b, b < c, a < c"""
        edges = [(a,b),(b,c),(a,c)]
        self.assertSort(edges)



if __name__ == '__main__':
    unittest.main()
