import pytest
from graph.graph_manager import GraphManager
from graph.graph import Graph
from graph.node import Node
import networkx as nx

# Test de Creación del Grafo
def test_create_graph():
    words = ["dog", "dig", "dot", "cat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Verifica que el grafo contiene el número correcto de nodos
    assert len(graph.graph.nodes) == 4  # Debería haber 4 nodos
    
    # Verifica que los nodos están conectados correctamente
    assert "dog" in graph.graph.neighbors("dot")
    assert "dot" in graph.graph.neighbors("dog")
    
    # Verifica que los nodos "cat" y "dog" no estén conectados (ya que difieren más de una letra)
    assert "cat" not in graph.graph.neighbors("dog")
    
# Test de Caminos Más Cortos
def test_shortest_path():
    words = ["dog", "dig", "dot", "cat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Verifica el camino más corto entre "dog" y "cat"
    shortest_path = graph.shortest_path("dog", "cat")
    assert shortest_path == ["dog", "dot", "cat"]  # El camino más corto es ["dog", "dot", "cat"]

# Test de Nodos Aislados
def test_isolated_nodes():
    words = ["dog", "dig", "dot", "cat", "bat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    isolated_nodes = graph.isolated_nodes()
    assert "bat" in isolated_nodes  # Se espera que "bat" sea aislado ya que no tiene conexiones con otras palabras

# Test de Clústeres
def test_clusters():
    words = ["dog", "dig", "dot", "cat", "bat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    clusters = graph.clusters()
    assert len(clusters) == 2  # Debería haber 2 clústeres, uno con "dog", "dig", "dot" y otro con "cat", "bat"

# Test de Conectividad de Nodos
def test_high_connectivity_nodes():
    words = ["dog", "dig", "dot", "cat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Busca nodos con al menos 2 conexiones
    high_connectivity_nodes = graph.high_connectivity_nodes(2)
    assert "dog" in high_connectivity_nodes  # "dog" tiene al menos 2 conexiones: "dot" y "dig"
    assert "dot" in high_connectivity_nodes  # "dot" tiene al menos 2 conexiones: "dog" y "cat"

# Test de Caminos Múltiples
def test_all_paths():
    words = ["dog", "dig", "dot", "cat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Verifica los caminos entre "dog" y "cat"
    all_paths = graph.all_paths("dog", "cat", max_depth=5)
    assert all_paths == [["dog", "dot", "cat"]]  # Debería haber un único camino que sea ["dog", "dot", "cat"]

# Test de Distancia Máxima
def test_maximum_distance():
    words = ["dog", "dig", "dot", "cat", "bat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Verifica la distancia máxima entre cualquier par de nodos en el grafo
    max_distance = graph.maximum_distance()
    assert max_distance == 2  # El máximo es 2, entre "dog" y "cat" pasando por "dot"

# Test de Nodos por Grado
def test_nodes_by_degree():
    words = ["dog", "dig", "dot", "cat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Verifica que los nodos con grado 2 son "dog", "dot" y "dig"
    degree_2_nodes = graph.nodes_by_degree(2)
    assert "dog" in degree_2_nodes
    assert "dot" in degree_2_nodes
    assert "dig" in degree_2_nodes
    assert "cat" not in degree_2_nodes  # "cat" tiene grado 1

# Test de Análisis del Grafo
def test_graph_analyzer():
    words = ["dog", "dig", "dot", "cat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Análisis básico del grafo
    analyzer = GraphAnalyzer(graph.graph)
    basic_info = analyzer.get_basic_info()
    assert basic_info['number_of_nodes'] == 4
    assert basic_info['number_of_edges'] == 3
    assert basic_info['average_degree'] == 1.5
    assert basic_info['number_of_connected_components'] == 1
    assert basic_info['largest_component_size'] == 4

# Test de Visualización del Grafo
def test_visualize_graph():
    words = ["dog", "dig", "dot", "cat"]
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Este test es más visual y no se puede comprobar con assert, pero se asegura que no lance errores
    analyzer = GraphAnalyzer(graph.graph)
    analyzer.visualize_graph(show_labels=True)  # Esto abrirá una ventana con el grafo visualizado

