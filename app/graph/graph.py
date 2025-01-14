# graph/graph.py

import networkx as nx
from .node import Node

class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, word: str):
        n = Node(word)
        self.graph.add_node(n)

    def add_edge(self, w1: str, w2: str) -> bool:
        n1 = Node(w1)
        n2 = Node(w2)
        if n1 not in self.graph:
            self.graph.add_node(n1)
        if n2 not in self.graph:
            self.graph.add_node(n2)
        if self._is_one_letter_apart(w1, w2):
            if not self.graph.has_edge(n1, n2):
                self.graph.add_edge(n1, n2)
                return True
        return False

    def _is_one_letter_apart(self, w1, w2):
        if len(w1) != len(w2):
            return False
        return sum(a != b for a, b in zip(w1, w2)) == 1

    def shortest_path(self, w1: str, w2: str):
        return nx.shortest_path(self.graph, Node(w1), Node(w2))

    def clusters(self):
        return list(nx.connected_components(self.graph))

    def high_connectivity_nodes(self, threshold: int):
        return [n for n in self.graph.nodes if self.graph.degree(n) >= threshold]

    def __repr__(self):
        return f"Graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges."

    def all_paths(self, w1: str, w2: str, max_depth: int = 15):
        """Encuentra todos los caminos posibles entre dos palabras con profundidad máxima."""
        try:
            n1, n2 = Node(w1), Node(w2)
            if n1 not in self.graph or n2 not in self.graph:
                return []
            return list(nx.all_simple_paths(self.graph, n1, n2, cutoff=max_depth))
        except nx.NetworkXNoPath:
            return []

    def maximum_distance(self):
        """Encuentra la distancia máxima entre cualquier par de nodos en el grafo."""
        max_dist = 0
        for component in nx.connected_components(self.graph):
            if len(component) > 1:
                subgraph = self.graph.subgraph(component)
                eccentricities = nx.eccentricity(subgraph)
                component_diameter = max(eccentricities.values())
                max_dist = max(max_dist, component_diameter)
        return max_dist

    def nodes_by_degree(self, degree: int):
        """Retorna los nodos con un grado específico de conectividad."""
        return [node for node, deg in self.graph.degree() if deg == degree]

    def isolated_nodes(self):
        """Retorna los nodos sin conexiones."""
        return list(nx.isolates(self.graph))