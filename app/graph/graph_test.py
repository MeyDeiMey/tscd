import pytest
from graph.graph import Graph
from graph.node import Node

# Test de creación de nodos
def test_add_node():
    graph = Graph()
    graph.add_node("dog")
    
    # Verifica que el nodo "dog" ha sido añadido correctamente
    assert len(graph.graph.nodes) == 1
    assert Node("dog") in graph.graph.nodes

# Test de adición de aristas
def test_add_edge():
    graph = Graph()
    graph.add_node("dog")
    graph.add_node("dot")
    
    # Verifica que la arista entre "dog" y "dot" se puede añadir
    assert graph.add_edge("dog", "dot") == True  # Debería añadir la arista
    assert graph.graph.has_edge(Node("dog"), Node("dot"))  # Verifica si la arista existe
    
    # Intenta añadir una arista entre dos nodos no conectados
    assert graph.add_edge("dog", "cat") == False  # "dog" y "cat" no están a un carácter de distancia

# Test de caminos más cortos
def test_shortest_path():
    graph = Graph()
    graph.add_node("dog")
    graph.add_node("dot")
    graph.add_node("cat")
    graph.add_edge("dog", "dot")
    graph.add_edge("dot", "cat")
    
    # Verifica el camino más corto entre "dog" y "cat"
    shortest_path = graph.shortest_path("dog", "cat")
    assert shortest_path == [Node("dog"), Node("dot"), Node("cat")]

# Test de clústeres
def test_clusters():
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
    assert Node("bat") in clusters[1]  # "bat" debe estar en el segundo clúster
    assert Node("cat") in clusters[0]  # "cat" debe estar en el primer clúster

# Test de nodos con alta conectividad
def test_high_connectivity_nodes():
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
    assert Node("cat") not in high_connectivity_nodes  # "cat" tiene solo 1 conexión

# Test de todos los caminos entre dos nodos
def test_all_paths():
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

# Test de distancia máxima
def test_maximum_distance():
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

# Test de nodos por grado
def test_nodes_by_degree():
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
    assert Node("dog") not in degree_2_nodes  # "dog" tiene grado 1

# Test de nodos aislados
def test_isolated_nodes():
    graph = Graph()
    graph.add_node("dog")
    graph.add_node("cat")
    graph.add_node("bat")
    
    # "bat" es un nodo aislado porque no tiene conexiones
    isolated_nodes = graph.isolated_nodes()
    assert Node("bat") in isolated_nodes  # "bat" está aislado
    assert Node("dog") not in isolated_nodes  # "dog" tiene una conexión
