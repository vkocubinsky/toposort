#!/usr/bin/env python3
from collections import OrderedDict

class CycleException(Exception):
    pass

class DepsManager:
    def __init__(self):
        self.deps = []

    def add_deps(self, before, after):
        self.deps.append((before,after))

    def sort(self):
        after_before_map, before_after_map = self._make_struct()
        ordered = []
        while after_before_map:
            first = self._find_first(after_before_map)
            if first is not None:
                self._clean(after_before_map, before_after_map, first)
                ordered.append(first)
            elif after_before_map:
                raise CycleException("Cycle found")
        return ordered    
                
    def _clean(self, after_before_map, before_after_map, first):
        assert first in after_before_map # first in nodes
        assert not after_before_map[first] # nodes[first] is empty
        
        del after_before_map[first]            
        for k in before_after_map[first].keys():
            del after_before_map[k][first]
        del before_after_map[first]

    def _find_first(self, nodes):
        for after, beforemap in nodes.items():
            if not beforemap:
                return after


    def _make_struct(self):
        after_before_map = OrderedDict() # nodes
        before_after_map = OrderedDict()
        for before,after in self.deps:
            # initialize after_before_map
            if after not in after_before_map:
                after_before_map[after]= OrderedDict()
            if before not in after_before_map:
                after_before_map[before] = OrderedDict()
            # initialize before_after_map    
            if after not in before_after_map:
                before_after_map[after]= OrderedDict()
            if before not in before_after_map:
                before_after_map[before] = OrderedDict()
    
            #put deps
            after_before_map[after][before] = 1
            before_after_map[before][after] = 1
        return after_before_map, before_after_map 




#    A -> B, B -> C
#    A      B      C
#    -      -      -
#           A      B


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

