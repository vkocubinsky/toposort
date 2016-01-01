#!/usr/bin/env python3
from collections import OrderedDict
from pprint import pprint

# TODO: add simple parser
# TODO: print first cycle
# TODO: distinguish < and <= 
    # test a < a cycle
    # test a <= a

class CycleException(Exception):
    pass

class GraphIndex:
    def __init__(self):
        # Nodes table wich keep list of before nodes.
        # a -> c, b -> c
        # {a: {}, b: {}, 'c': {'a':1, 'b':1}}
        self.before_table = OrderedDict()
        
        # Nodes table wich keep list of after nodes.
        # a -> c, b -> c
        # {'a': {'c':1}, 'b': {'c':1}, c: {}}
        self.after_table = OrderedDict() 


        # Nodes with empty before table
        # a -> c, b -> c
        # {'a':1, 'b':1}
        self.zero_table = OrderedDict() 

    def table__str__(self, table):
        ts = ["\n    {k}: {vs}".format(k=k,vs=list(v.keys())) 
                for k,v in table.items()]
        return "".join(ts)

    def __str__(self):
        return """GraphIndex(
Before Table: {before_table}
After Table: {after_table}
Zero Set: {zero_table})""".format(
            before_table=self.table__str__(self.before_table),
            after_table=self.table__str__(self.after_table),
            zero_table=list(self.zero_table.keys())    
                )

    def add(self, before, after):
        # Initialize before_table
        if after not in self.before_table:
            self.before_table[after] = OrderedDict()
            self.zero_table[after] = 1
        if before not in self.before_table:
            self.before_table[before] = OrderedDict()
            self.zero_table[before] = 1
        # Initialize after_table    
        if after not in self.after_table:
            self.after_table[after] = OrderedDict()
        if before not in self.after_table:
            self.after_table[before] = OrderedDict()

        # Put deps
        if after != before:
            self.before_table[after][before] = 1
            self.after_table[before][after] = 1

        if after != before and after in self.zero_table:
            del self.zero_table[after]

    def pop_zero(self):
        if self.zero_table:
            first = self.zero_table.popitem(last=False)
            self.remove(first[0])
            return first[0]


    def remove(self, first):
        assert first in self.before_table, "{} not in {}".format(first, self.before_table)
        assert not self.before_table[first]
        
        del self.before_table[first]            
        for k in self.after_table[first].keys():
            del self.before_table[k][first]
            if not self.before_table[k]:
                self.zero_table[k] = 1
        del self.after_table[first]

def graph_from_edges(edges):
    g = Graph()
    for edge in edges:
        g.add_edge(*edge)
    return g

def sort_edges(edges):
    g = graph_from_edges(edges)
    return g.sort()

class Graph:
    def __init__(self):
        self.edges = []

    def add_edge(self, before, after):
        self.edges.append((before,after))

    def sort(self):
        index = GraphIndex()
        for before,after in self.edges:
            index.add(before,after)
        ordered = []
        while True:
            first = index.pop_zero()
            if first:    
                ordered.append(first)
            else:
                break
        if index.before_table:
            raise CycleException("Cycle found")
        return ordered    

