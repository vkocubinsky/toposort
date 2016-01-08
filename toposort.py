#!/usr/bin/env python3
from collections import OrderedDict
import fileinput

# TODO: support None value, test none as other elements
# TODO: yield
# TODO: fill readme

class CycleException(Exception):

    def __init__(self,cycle):
        Exception.__init__(self,cycle)
        self.cycle = cycle

class GraphIndex:
    def __init__(self):
        # a -> c, b -> c
        # {'a': {'c':1}, 'b': {'c':1}, c: {}}
        self.next_table = OrderedDict() 

        # a -> c, b -> c
        # {a: {}, b: {}, 'c': {'a':1, 'b':1}}
        self.prev_table = OrderedDict()
        
        # Nodes with no previous 
        # a -> c, b -> c
        # {'a':1, 'b':1}
        self.zero_table = OrderedDict() 


    def __str__(self):

        def table__str__(table):
            ts = ["\n    {k}: {vs}".format(k=k,vs=list(v.keys())) 
                    for k,v in table.items()]
            return "".join(ts)

        return """GraphIndex(
Next Table: {next_table}
Prev Table: {prev_table}
Zero Set: {zero_table})""".format(
            prev_table=table__str__(self.prev_table),
            next_table=table__str__(self.next_table),
            zero_table=list(self.zero_table.keys())    
                )

    def add(self, n1, n2):
        self.next_table.setdefault(n1,OrderedDict())
        self.next_table.setdefault(n2,OrderedDict())

        self.prev_table.setdefault(n1,OrderedDict())
        self.prev_table.setdefault(n2,OrderedDict())

        if n2 != n1:
            self.next_table[n1][n2] = 1
            self.prev_table[n2][n1] = 1

        if not self.prev_table[n1]:
            self.zero_table[n1] = 1
        if not self.prev_table[n2]:
            self.zero_table[n2] = 1
        elif n2 in self.zero_table:
            del self.zero_table[n2]


    def remove(self, n1):
        assert n1 in self.prev_table
        assert n1 in self.next_table
        assert not self.prev_table[n1]
        
        del self.prev_table[n1]            
        for n2 in self.next_table[n1].keys():
            del self.prev_table[n2][n1]
            if not self.prev_table[n2]:
                self.zero_table[n2] = 1
        del self.next_table[n1]

    def first_cycle(self):
        assert self.prev_table
        assert self.next_table
        cycle = OrderedDict()
        n = next(iter(self.next_table))
        while self.next_table[n]:
            if n in cycle:
                return list(cycle.keys())
            else:
                cycle[n]=1
                n = next(iter(self.next_table[n]))
        raise AssertionError('Cycle not found') 


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

    def add_edge(self, n1, n2):
        self.edges.append((n1,n2))

    def sort(self):
        index = GraphIndex()
        for n1,n2 in self.edges:
            index.add(n1,n2)
        ordered = []
        while index.zero_table:
            n0,_one = index.zero_table.popitem(last=False)
            index.remove(n0)
            ordered.append(n0)
        if index.prev_table:
            raise CycleException(index.first_cycle())
        return ordered    

if __name__ == '__main__':
    """Like unix tsort"""
    g = Graph()
    for line in fileinput.input():
        n1, n2 = line.split() 
        g.add_edge(n1, n2)
    for n in g.sort():
        print(n)

