class EdgeSet:

    def __init__(self):
        self.edges = [] 

    def __str__(self):
        return str(self.edges)

    def __and__(self, other):
        if isinstance(other, Edge):
            self.edges.append(other)
            return self
        else:
            return NotImplemented

    def __iter__(self):
        return iter(self.edges)

class Edge:

    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

    def __str__(self):
        return "{self.n1.value} << {self.n2.value}".format(self=self)

    def __and__(self, other):
        if isinstance(other, Edge):
            s = EdgeSet()
            return s & other
        else:
            return NotImplemented

class Node:

    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.value)
   
    def __lshift__(self, other):
        if isinstance(other,Node):
            return Edge(self,other)
        else:
            return NotImplemented

    def __rshift__(self, other):
        if isinstance(other,Node):
            return Edge(other,self)
        else:
            return NotImplemented

def from_list(xs):
    return [Node(x) for x in xs]
