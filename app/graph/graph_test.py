import unittest
import networkx as nx
from graph.graph import Graph
from graph.node import Node

class TestGraph(unittest.TestCase):

    def test_shortest_path(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("dot")
        graph.add_node("cat")
        graph.add_edge("dog", "dot")
        graph.add_edge("dot", "cat")

        # Verifica el camino más corto entre "dog" y "cat"
        shortest_path = graph.shortest_path("dog", "cat")
        self.assertEqual(shortest_path, ["dog", "dot", "cat"])

    def test_clusters(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("dot")
        graph.add_node("cat")
        graph.add_node("bat")
        graph.add_edge("dog", "dot")
        graph.add_edge("dot", "cat")

        # Verifica los clústeres del grafo
        clusters = graph.clusters()
        self.assertEqual(len(clusters), 2)  # Deberían haber 2 clústeres

    def test_high_connectivity_nodes(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("dot")
        graph.add_node("cat")
        graph.add_node("bat")
        graph.add_edge("dog", "dot")
        graph.add_edge("dot", "cat")
        graph.add_edge("dot", "bat")

        # Busca nodos con al menos 2 conexiones
        high_connectivity_nodes = graph.high_connectivity_nodes(2)
        self.assertIn(Node("dot"), high_connectivity_nodes)  # "dot" tiene 3 conexiones

    def test_all_paths(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("dot")
        graph.add_node("cat")
        graph.add_node("bat")
        graph.add_edge("dog", "dot")
        graph.add_edge("dot", "cat")

        # Verifica que el único camino entre "dog" y "cat" es ["dog", "dot", "cat"]
        all_paths = graph.all_paths("dog", "cat", max_depth=3)
        self.assertEqual(all_paths, [["dog", "dot", "cat"]])

    def test_maximum_distance(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("dot")
        graph.add_node("cat")
        graph.add_node("bat")
        graph.add_edge("dog", "dot")
        graph.add_edge("dot", "cat")
        graph.add_edge("dot", "bat")

        # Verifica la distancia máxima entre los nodos
        max_distance = graph.maximum_distance()
        self.assertEqual(max_distance, 2)  # La distancia máxima es 2 entre "dog" y "cat" pasando por "dot"

    def test_nodes_by_degree(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("dot")
        graph.add_node("cat")
        graph.add_node("bat")
        graph.add_edge("dog", "dot")
        graph.add_edge("dot", "cat")
        graph.add_edge("dot", "bat")

        # Verifica los nodos con grado 2 (en este caso, "dot")
        degree_2_nodes = graph.nodes_by_degree(2)
        self.assertIn(Node("dot"), degree_2_nodes)  # "dot" tiene grado 3

    def test_isolated_nodes(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("cat")
        graph.add_node("bat")

        # "bat" es un nodo aislado porque no tiene conexiones
        isolated_nodes = graph.isolated_nodes()
        self.assertIn(Node("bat"), isolated_nodes)  # "bat" está aislado
        self.assertNotIn(Node("dog"), isolated_nodes)  # "dog" tiene una conexión

if __name__ == '__main__':
    unittest.main()
