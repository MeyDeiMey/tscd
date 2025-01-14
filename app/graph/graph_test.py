import pytest
from graph.graph_manager import GraphManager
from graph.graph import Graph
from graph.graph_analyzer import GraphAnalyzer

# Lista de palabras que cumplen con la regla de diferencia máxima de 3 letras
words = [
    "dog", "dot", "dig", "cat", "bat", "rat", "hat", "pat", "mat", "sat", "fat", "lot",
    "log", "fog", "cog", "pot", "hot", "not", "got", "bot", "lot"
]

# Test de Creación del Grafo
def test_create_graph():
    graph_manager = GraphManager()
    graph_manager.build_graph(words)  # Construcción del grafo
    graph = graph_manager.get_graph()  # Obtención del grafo
    
    # Verifica que el grafo contiene el número correcto de nodos
    assert len(graph.graph.nodes) == len(words)  # Debería haber 20 nodos
    
    # Verifica que "dog" y "dot" están conectados
    assert "dog" in graph.graph.neighbors("dot")
    assert "dot" in graph.graph.neighbors("dog")
    
    # Verifica que "dog" y "cat" no están conectados
    assert "cat" not in graph.graph.neighbors("dog")


# Test de Caminos Más Cortos
def test_shortest_path():
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Verifica el camino más corto entre "dog" y "cat"
    shortest_path = graph.shortest_path("dog", "cat")
    assert shortest_path == ["dog", "dot", "cat"]  # El camino más corto es ["dog", "dot", "cat"]


# Test de Nodos Aislados
def test_isolated_nodes():
    words.append("xyz")  # Añadimos una palabra aislada
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    isolated_nodes = graph.isolated_nodes()
    assert "xyz" in isolated_nodes  # "xyz" debería ser aislada


# Test de Clústeres
def test_clusters():
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    clusters = graph.clusters()
    assert len(clusters) == 2  # Se espera que haya dos clústeres principales


# Test de Conectividad de Nodos
def test_high_connectivity_nodes():
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Busca nodos con al menos 3 conexiones
    high_connectivity_nodes = graph.high_connectivity_nodes(3)
    assert "dog" in high_connectivity_nodes
    assert "dot" in high_connectivity_nodes


# Test de Caminos Múltiples
def test_all_paths():
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Verifica los caminos entre "dog" y "cat"
    all_paths = graph.all_paths("dog", "cat", max_depth=5)
    assert all_paths == [["dog", "dot", "cat"]]  # Debería haber un único camino que sea ["dog", "dot", "cat"]


# Test de Distancia Máxima
def test_maximum_distance():
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Verifica la distancia máxima entre cualquier par de nodos en el grafo
    max_distance = graph.maximum_distance()
    assert max_distance == 2  # La distancia máxima es 2 entre "dog" y "cat"


# Test de Nodos por Grado
def test_nodes_by_degree():
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Verifica que los nodos con grado 3 son aquellos con múltiples conexiones
    degree_3_nodes = graph.nodes_by_degree(3)
    assert "dog" in degree_3_nodes
    assert "dot" in degree_3_nodes
    assert "cat" not in degree_3_nodes  # "cat" tiene grado 2, no 3


# Test de Análisis del Grafo
def test_graph_analyzer():
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Análisis básico del grafo
    analyzer = GraphAnalyzer(graph.graph)
    basic_info = analyzer.get_basic_info()
    assert basic_info['number_of_nodes'] == len(words)
    assert basic_info['number_of_edges'] == 19
    assert basic_info['average_degree'] == 1.9
    assert basic_info['number_of_connected_components'] == 1
    assert basic_info['largest_component_size'] == len(words)


# Test de Visualización del Grafo
def test_visualize_graph():
    graph_manager = GraphManager()
    graph_manager.build_graph(words)
    graph = graph_manager.get_graph()
    
    # Este test es más visual y no se puede comprobar con assert, pero se asegura que no lance errores
    analyzer = GraphAnalyzer(graph.graph)
    analyzer.visualize_graph(show_labels=True)  # Esto abrirá una ventana con el grafo visualizado

