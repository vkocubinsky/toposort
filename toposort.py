#!/usr/bin/env python3
from collections import OrderedDict
from pprint import pprint

# TODO: add simple parser
# TODO: add tests and exampes
# TODO: print first cycle

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
        assert before != after
        # initialize before_table
        if after not in self.before_table:
            self.before_table[after] = OrderedDict()
            self.zero_table[after] = 1
        if before not in self.before_table:
            self.before_table[before] = OrderedDict()
            self.zero_table[before] = 1
        # initialize after_table    
        if after not in self.after_table:
            self.after_table[after] = OrderedDict()
        if before not in self.after_table:
            self.after_table[before] = OrderedDict()

        #put deps
        self.before_table[after][before] = 1
        self.after_table[before][after] = 1

        if after in self.zero_table:
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

class DepsManager:
    def __init__(self):
        self.deps = []

    def add_deps(self, before, after):
        self.deps.append((before,after))

    def sort(self):
        index = GraphIndex()
        for before,after in self.deps:
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


# Right Topologies a,b,c
# no lines: a, b, c
# 2 line: a < b, c
# 3 line: a < b < c
# split : a < (b,c)
# join : (a,b) < c   
 
# Cycles
# 1 line cycle: a < a, b, c
# 2 line cycle: a < b < a, c
# 3 line cycle: a < b < c < a

# Mix
# join and cycle either: (a,b) < c, c < a, c < b
# join and cycle one: (a,b) < c, c < a
# split and cycle either: a < (b,c), b < a, c < a 
# split and cycle one: a < (b,c), b < a



if __name__ == '__main__':
    print("Started")
    try:
        d = DepsManager()
        d.add_deps(1,2)
        d.add_deps(2,3)
        d.add_deps(2,5)
        d.add_deps(4,6)
        print("ordered", d.sort())
        #cycle
        d.add_deps(3,1)
        print("ordered", d.sort())
    except CycleException as e:
        print("Cycle found", e)

