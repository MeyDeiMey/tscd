import pytest
from graph.graph import Graph
from graph.node import Node

class TestGraph:
    def test_shortest_path(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("dot")
        graph.add_node("cat")
        graph.add_edge("dog", "dot")
        graph.add_edge("dot", "cat")

        # Verifica el camino más corto entre "dog" y "cat"
        shortest_path = graph.shortest_path("dog", "cat")
        assert shortest_path == ["Node(dog)", "Node(dot)", "Node(cat)"]

    def test_clusters(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("dot")
        graph.add_node("cat")
        graph.add_node("bat")

        graph.add_edge("dog", "dot")
        graph.add_edge("dot", "cat")

        # Debería haber 2 clústeres: uno con "dog", "dot", "cat" y otro con "bat"
        clusters = graph.clusters()
        assert len(clusters) == 2

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
        assert Node("dot") in high_connectivity_nodes  # "dot" tiene 3 conexiones

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
        assert all_paths == [["dog", "dot", "cat"]]

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
        assert max_distance == 2  # La distancia máxima es 2 entre "dog" y "cat" pasando por "dot"

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
        assert Node("dot") in degree_2_nodes  # "dot" tiene grado 3

    def test_isolated_nodes(self):
        graph = Graph()
        graph.add_node("dog")
        graph.add_node("cat")
        graph.add_node("bat")

        # "bat" es un nodo aislado porque no tiene conexiones
        isolated_nodes = graph.isolated_nodes()
        assert Node("bat") in isolated_nodes  # "bat" está aislado
        assert Node("dog") not in isolated_nodes  # "dog" tiene una conexión
