import unittest
from Graph import *

# The weight I will be using is the distance between cities along roads, the data for which I got from
# google maps.
#
#
#                                           ascii art of my graph:
#
#                                                  Boston
#                                                /       \ 
#                                      103.3 mi /         \ 106.9 mi
#                                              /   51.4 mi \
#                                         Hartford ------ New London
#                                        /      \               / 
#                               116.3 mi/        \ 38.9 mi     / 47.8 mi
#                                      / 80.7 mi  \           /
#                                 N.Y.C ----------- New Haven
#                                /     \
#                       20.1 mi /       \ 25.8 mi
#                              / 53.6 mi \
#                        Maplewood ------ Garden City

cities = ['Boston', 'Hartford', 'New London', 'New York City', 'New Haven', 'Maplewood', 'Garden City']


        
# edges are in the format (vertex1, vertex2, weight)
# weight being the distance between vertex1 and vertex2

edges = [('Boston', 'Hartford', 103.3), 
        ('Boston', 'New London', 106.9), 
        ('New London', 'Boston', 106.9), 
        ('New London', 'Hartford', 51.4), 
        ('New London', 'New Haven', 47.8), 
        ('Hartford', 'Boston', 103.3), 
        ('Hartford', 'New London', 51.4), 
        ('Hartford', 'New Haven', 38.9), 
        ('Hartford', 'New York City', 116.3), 
        ('New Haven', 'Hartford', 38.9), 
        ('New Haven', 'New London', 47.8), 
        ('New Haven', 'New York City', 80.7), 
        ('New York City', 'Hartford', 116.3), 
        ('New York City', 'New Haven', 80.7), 
        ('New York City', 'Garden City', 25.8), 
        ('New York City', 'Maplewood', 20.1), 
        ('Maplewood', 'Garden City', 53.6), 
        ('Maplewood', 'New York City', 20.1),
        ('Garden City', 'Maplewood', 53.6),
        ('Garden City', 'New York City', 25.8)]


class TestGraph(unittest.TestCase):
    
    # regular graph ADT tests for adding/removing vertices/edges
    
    def test_add_remove_vertices(self):
        
        # initialize graph
        city_graph = Graph()
        
        for city in cities:
            city_graph.add_vertex(city)

        for city in cities:
            # make sure that each city was properly added to graph
            assert city in city_graph.V
        
        # check that remove_vertex behaves as expected
        city_graph.remove_vertex('New London')
        assert not 'New London' in city_graph.V
        
        
    def test_add_remove_edges(self):
        print()
        print("showing all vertices and their neighbors")

        
        # initialize graph
        city_graph = Graph()
                
        for city in cities:
            city_graph.add_vertex(city)
        
        # add each edge to the graph
        for entry in edges:
            city_graph.add_edge(entry)
        
        # print each vertex's neighbors to verify that each vertex has the correct edges
        for v in city_graph:
            print("city = {}, neighbors:".format(v))
            for nbr in city_graph._neighbors(v):
                print("\t{}".format(nbr))
            print()
        
        # remove some edges
        city_graph.remove_edge(('Garden City', 'Maplewood', 53.6))
        city_graph.remove_edge(('Garden City', 'New York City', 25.8))
        
        # make sure that Garden city now has no edges
        num_nbrs = 0
        for nbr in city_graph._neighbors('Garden City'):
            num_nbrs += 1
        
        assert num_nbrs == 0
        
    
    # Test weighted portion of Graph
    
    def test_weight(self):
        # initialize graph
        city_graph = Graph()
                
        for city in cities:
            city_graph.add_vertex(city)
        
        for entry in edges:
            city_graph.add_edge(entry)

        # check that weight returns correct values
        assert city_graph.weight(('Garden City', 'Maplewood')) == 53.6
        assert city_graph.weight(('Boston', 'Hartford')) == 103.3
        assert not city_graph.weight(('New Haven', 'Hartford')) == 500
    
    def test_fewest_edges(self):
        # initialize graph
        city_graph = Graph()
                
        for city in cities:
            city_graph.add_vertex(city)
        
        for entry in edges:
            city_graph.add_edge(entry)
        
        # check if dict returned is correct: format is that keys are the vertex, and values are the previously visited vertex
        assert city_graph.bfs('Boston') == {'Boston': None, 'Hartford': 'Boston', 'New London': 'Boston', 'New Haven': 'Hartford', 'New York City': 'Hartford', 'Garden City': 'New York City', 'Maplewood': 'New York City'}
    
    def test_lowest_cost(self):
        # initialize graph
        city_graph = Graph()
                
        for city in cities:
            city_graph.add_vertex(city)
        
        for entry in edges:
            city_graph.add_edge(entry)

        # This algorithm returns the table in which the key is the vertex, and the value is a tuple containing
        # (smallest distance to source, previous vertex)
        assert(city_graph.lowest_cost('Hartford')) == {'Boston': (103.3, 'Hartford'), 'Garden City': (142.1, 'New York City'), 'New Haven': (38.9, 'Hartford'), 'New London': (51.4, 'Hartford'), 'Maplewood': (136.4, 'New York City'), 'Hartford': (0, None), 'New York City': 
              (116.3, 'Hartford')}
        
        # verify that it still works for a different graph
        city_graph.remove_edge(('Hartford', 'New London', 51.4))
        city_graph.remove_edge(('New London', 'Hartford', 51.4))
        
        assert city_graph.lowest_cost('Hartford') == {'New Haven': (38.9, 'Hartford'), 'Hartford': (0, None), 'New London': (86.69999999999999, 'New Haven'), 'Garden City': (142.1, 'New York City'), 'New York City': (116.3, 'Hartford'), 'Boston': (103.3, 'Hartford'), 'Maplewood': (136.4, 'New York City')}
        
    def test_lowest_total(self):
        # initialize graph
        city_graph = Graph()
                
        for city in cities:
            city_graph.add_vertex(city)
        
        for entry in edges:
            city_graph.add_edge(entry)
        
        # this algorithm returns a tuple where the first item is a table where each vertex is a key and the value is the vertex's 'parent'.
        # It also returns the total distance of the MST as the second item in the tuple
        assert city_graph.lowest_total('New London') == ({'Garden City': 'New York City', 'Boston': 'Hartford', 'New York City': 'New Haven', 'Hartford': 'New Haven', 'New Haven': 'New London', 'New London': None, 'Maplewood': 'New York City'}, 316.59999999999997)
        
        # verify it still works for a different graph
        city_graph.remove_edge(('Garden City', 'New York City', 25.8))
        city_graph.remove_edge(('New York City', 'Garden City', 25.8))
        
        assert city_graph.lowest_total('New London') == ({'New Haven': 'New London', 'Hartford': 'New Haven', 'Garden City': 'Maplewood', 'Maplewood': 'New York City', 'Boston': 'Hartford', 'New London': None, 'New York City': 'New Haven'}, 344.4)
    
if __name__ == '__main__':
    unittest.main()