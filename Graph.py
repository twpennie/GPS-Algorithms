import math # for infinity

# the Graph will use an adjacency set and will have to have a weight function in order
# to give edges the distance between cities.

class Graph:
    def __init__(self):
        self.V = set()
        self.nbrs = dict()

    def add_vertex(self, v):
        self.V.add(v)
        self.nbrs[v] = {}
        
    def remove_vertex(self, v):
        self.V.remove(v)

    def add_edge(self, e):
        # slight change from regular graph ADT to account for weight
        u, v, weight = e
        self.nbrs[u][v] = weight
        
    def remove_edge(self, e):
        u, v, weight = e
        del self.nbrs[u][v]
    
    def weight(self, e):
        u, v = e
        return self.nbrs[u][v]

    def __iter__(self):
        return iter(self.V)

    def _neighbors(self, v):
        return iter(self.nbrs[v])
    
    # Breadth-First-Search for use in fewest_edges method
    def bfs(self, v):
        tree = {}              # child:parent pairs
        to_visit = [(None, v)] # parent, child tuples

        while to_visit:
            a, b = to_visit.pop(0) # a, b = (parent, child)
            if b not in tree:
                tree[b] = a # child:parent pairs
                for n in self._neighbors(b):
                    if n not in tree: to_visit.append((b, n))

        return tree 
    
    
    def fewest_edges(self, source):
        # Connects each city from a given source with the fewest number of edges
        # this can just peform a breadth-first-search to find this information, as
        # we do not need to account for weight
        return self.bfs(source)

    def lowest_cost(self, source):
        # Connects each city from a given source with the lowest cost from that source
        # Now we must account for weight, and therefore will use Dijkstra's shortest path algorithm
        
        # initialize some starting variables
        table = {} # will hold results, keys are the vertex's of the graph and items will be tuples: (shortest distance, previous vertex)
        for vertex in self.V:
            if vertex == source:
                # Let distance of start vertex to iteself = 0
                table[vertex] = (0, None)
            else:
                # Let distance of all other vertices from start = infinity
                table[vertex] = (math.inf, None)
        
        unvisited = set()
        for vertex in self.V:
            unvisited.add(vertex)

        visited = set()
        
        # Repeat until all vertices visited:
        while len(unvisited) != 0:
            
        # 1. visit the unvisited vertex with the smallest known distnace from the source
            smallest_known = None
            for vertex in unvisited:
                if smallest_known is None or table[vertex][0] < table[smallest_known][0]:
                    smallest_known = vertex
                
        # 2. for the current vertex, loop through its unvisited neighbors
            for nbr in self._neighbors(smallest_known):
                if nbr not in unvisited:
                    continue
                
        # 3. for the current vertex, calculate distance of each neighbor from the source
                distance = table[smallest_known][0] + self.weight((nbr, smallest_known))
                
        # 4. if the calculated distance of a vertex is less than the known distance, update
        # the shortest distance and previous vertex
                if distance < table[nbr][0]:
                    table[nbr] = (distance, smallest_known)
                    
        # 5. add the current vertex to the list of visited vertices
            visited.add(smallest_known)
            unvisited.remove(smallest_known)
        
        return table
        
    
    def lowest_total(self, source):
        # Connects each city from a given source with the lowest total cost
        # For this we will use Prim's Minimium Spanning Tree Algorithm
        
        # initialize some starting variables:
        visited = set()
        unvisited = set()
        
        tree = {} # holds the results: tree will be formatted so that keys are vertices and values are
                  # the parent vertices
                  
        for vertex in self.V:
            tree[vertex] = None
        
        total = 0 # total edge weight of the tree
        
        for vertex in self.V:
            unvisited.add(vertex)
        

        # start at source vertex: continue until all nodes are visited
        visited.add(source)
        unvisited.remove(source)
        
        
        while len(unvisited) != 0:
            
        # 1. examine all vertices reachable from visited vertices
        # 2. find the smallest edge that connects to an unvisited vertex
        
            smallest_edge = (None, None, math.inf) # format: child, parent, distance
            
            for v in visited:
                for nbr in self._neighbors(v):
                    if nbr not in visited:
                        if self.weight((v, nbr)) < smallest_edge[2]:
                            smallest_edge = (nbr, v, self.weight((v, nbr)))
        
        # 3. add that node to visited and remove from unvisited
            child, parent, distance = smallest_edge
            visited.add(child)
            unvisited.remove(child)
            
            tree[child] = parent
            
            total += distance
        
        return (tree, total)
            
        
        