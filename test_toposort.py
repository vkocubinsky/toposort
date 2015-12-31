#!/usr/bin/env python3
import unittest

from toposort import *


# Right Topologies a,b,c
# no lines: a = a, b = b, c = c
# 2 line: a < b, c = c
# => CURSOR
# 3 line: a < b < c
# split : a < (b,c)
# join : (a,b) < c   
 
# Cycles
# 1 line cycle: a < a, b = b, c = c
# 2 line cycle: a < b < a, c = c
# 3 line cycle: a < b < c < a

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
class TestGraphIndex(unittest.TestCase):

  def test_no_lines(self):
      """ no lines: a = a, b = b, c = c"""
      g = Graph()
      g.add_edge('a','a')
      g.add_edge('b','b')
      g.add_edge('c','c')

      ordered = g.sort()
      self.assertEqual(3, len(ordered))
      self.assertTrue(all([x in ordered for x in 'abc']))

  def test_2_line(self):
      """ 2 line: a < b, c = c """
      g = Graph()
      g.add_edge('a','b')
      g.add_edge('c','c')

      ordered = g.sort()
      self.assertEqual(3, len(ordered))
      self.assertTrue(all([x in ordered for x in 'abc']))
      self.assertTrue(ordered.index('a') < ordered.index('b')) 


  def test_split(self):
      s = 'hello world'
      self.assertEqual(s.split(), ['hello', 'world'])
      # check that s.split fails when the separator is not a string
      with self.assertRaises(TypeError):
          s.split(2)

if __name__ == '__main__':
    unittest.main()
