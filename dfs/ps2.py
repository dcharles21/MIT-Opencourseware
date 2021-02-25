# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

# Finding shortest paths through MIT buildings
import sys 
import unittest
from graph import Digraph, Node, WeightedEdge

# Problem 2: Building up the Campus Map

# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    
    print("Loading map from file...")
    print(" ")

    g = Digraph()

    f = open(map_filename, 'r')
    for line in f:

        map = line.split()

        src = Node(str(map[0]))
        dest = Node(str(map[1]))
        total_dist = int(map[2])
        outdoor_dist = int(map[3])

        if not g.has_node(src):
            g.add_node(src)
        
        if not g.has_node(dest):
            g.add_node(dest)

        e =  WeightedEdge(src, dest, total_dist, outdoor_dist)

        g.add_edge(e)     
              

    f.close()

    return g

# Problem 3: Finding the Shorest Path using Optimized Search Method

# Problem 3b: Implement get_best_path

def printPath(path):
    """ Assumes path is a list of nodes """    
    
    result = ''
    for i in range(len(path)):        
        result = result + str(path[i])        
        
        if i != len(path) - 1:
            result = result + '->'
    
    return result
  
def get_best_path(digraph, start, end, path, best_path, dist, best_dist, max_dist_outdoors):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search

        start: string
            Building number at which to start

        end: string
            Building number at which to end

        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.

        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end

        represented by a list of building numbers (in strings):
            [n_1, n_2, ..., n_k]; there exists an edge from n_i to n_(i+1)
            in digraph for all 1 <= i < k-1 and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """   
    if not (digraph.has_node(start) or digraph.has_node(end)):
        raise ValueError('No such node in graph')

    path = path + [start]

    print('Current DFS path:', printPath(path))
    print('Distance Travelled:', dist)
    print('Remaining Outdoor Distance:', max_dist_outdoors)
    print(" ")


    if start == end:
        best_dist = dist
        best_path = (path, best_dist, max_dist_outdoors)

        return best_path

    # First check if child is in path
    # Then check if distance is good
    # If everything checks out go to child node

    for child in digraph.get_edges_for_node(start):        

        if child not in path:

            dist += digraph.get_dist(start, child)[0]
            max_dist_outdoors -= digraph.get_dist(start, child)[1]

            if dist <= best_dist and max_dist_outdoors >= 0:


                best_path = get_best_path(digraph, child, end, path, best_path, dist, best_dist, max_dist_outdoors)     

                dist -= digraph.get_dist(start, child)[0]
                max_dist_outdoors += digraph.get_dist(start, child)[1]           

                if best_path != None:
                    best_dist = best_path[1]
                
            else:
                dist -= digraph.get_dist(start, child)[0]
                max_dist_outdoors += digraph.get_dist(start, child)[1]         

    return best_path        

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors I suppose

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search

        start: string
            Building number at which to start

        end: string
            Building number at which to end

        max_total_dist: int
            Maximum total distance on a path

        max_dist_outdoors: int
            Maximum distance spent outdoors on a path I suppose

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    start = Node(start)
    end = Node(end)
    path = []    
    best_path = None    
    dist = 0
    best_dist = max_total_dist

    sp = get_best_path(digraph, start, end, path, best_path, dist, best_dist, max_dist_outdoors)

    if sp == None:
        raise ValueError('No path found')

    path = []
    for node in sp[0]:
        path.append(str(node))               

    return path

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        # all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)

if __name__ == "__main__":
    unittest.main()

    # map = load_map('test_graph.txt')
    # sp = get_best_path(map, start = Node(0), end = Node(5), path = [], best_path = None, dist = 0, best_dist = 10, outdoor_dist = 0, max_dist_outdoors = 15)  
    # print(sp)

    # map = load_map('test_graph.txt')
    # sp = get_best_path(map, start = Node(2), end = Node(3), path = [], best_path = None, dist = 0, best_dist = 10, outdoor_dist = 0, max_dist_outdoors = 0)  
    # print(sp)


    # map = load_map('test_graph.txt')
    # sp = directed_dfs(map, start = '0', end = '5', max_total_dist = 10, max_dist_outdoors = 15)  
    # print(sp)    
