#!/usr/bin/env python3
from collections import OrderedDict

nodes = OrderedDict()

class DepsManager:
    def __init__(self):
        self.deps = []
        self.ordered = []

    def add_deps(self, before, after):
        self.deps.append((before,after))

    def sort(self):
        nodes = self._make_struct()
        while True:
            first = self._find_first(nodes)
            if first is not None:
                self._clean(nodes, first)
                self.ordered.append(first)
            elif nodes:
                print("Cycles")
                break
            else:
                print("No Cycles")
                break
                
    def _clean(self, nodes, first):
        assert first in nodes # first in nodes
        assert not nodes[first] # nodes[first] is empty
        del nodes[first]            
        for after, beforemap in nodes.items():
            if first in beforemap:
                del beforemap[first]

    def _find_first(self, nodes):
        for after, beforemap in nodes.items():
            if not beforemap:
                return after


    def _make_struct(self):
        nodes = OrderedDict()
        for before,after in self.deps:
            #todo: lazy add
            if before not in nodes:
                nodes[before] = OrderedDict()
            if after not in nodes:
                nodes[after]= OrderedDict()
            #put deps
            nodes[after][before] = 1
        return nodes 




#    A -> B, B -> C
#    A      B      C
#    -      -      -
#           A      B


if __name__ == '__main__':
    print("Started")
    d = DepsManager()
    d.add_deps(1,2)
    d.add_deps(2,3)
    d.add_deps(2,5)
    d.add_deps(4,6)
    #cycle
    d.add_deps(3,1)
    d.sort()
    print("ordered", d.ordered)

