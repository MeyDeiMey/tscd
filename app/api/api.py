from flask import Flask, request, jsonify
import os
import sys
import boto3
import json
import networkx as nx

# Asegurarse de que Python reconozca la carpeta raíz del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.graph import Graph

app = Flask(__name__)

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
BUCKET_NAME = "graphword-datamart-bucket"
TABLE_NAME = "GraphNodes"

graph = Graph()
is_initialized = False

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Bienvenido a la API de Grafos",
        "endpoints": {
            "POST /initialize": "Construye el grafo a partir de datos en S3",
            "GET /shortest-path?word1=...&word2=...": "Obtiene el camino más corto entre dos palabras",
            "GET /clusters": "Retorna los componentes conectados del grafo",
            "GET /high-connectivity?degree=2": "Retorna los nodos con grado >= 2"
        }
    })

@app.route("/initialize", methods=["POST"])
def initialize_graph():
    global is_initialized
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix="words_")
        files = response.get('Contents', [])
        if not files:
            return jsonify({"error": "No se encontraron archivos en el bucket S3."}), 400

        all_words = set()
        for file in files:
            obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=file['Key'])
            content = obj['Body'].read().decode('utf-8')
            for line in content.splitlines():
                word = line.strip()
                if word:
                    all_words.add(word)

        # Construir el grafo
        for word in all_words:
            graph.add_node(word)

        # Crear relaciones entre nodos (opcional: ajustar lógica)
        word_list = list(all_words)
        for i in range(len(word_list)):
            for j in range(i + 1, len(word_list)):
                w1, w2 = word_list[i], word_list[j]
                graph.add_edge(w1, w2)

        # Persistir nodos y relaciones en DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        for word in all_words:
            connected_nodes = list(graph.neighbors(word))
            table.put_item(Item={
                'node': word,
                'connected_nodes': json.dumps(connected_nodes)
            })

        is_initialized = True
        return jsonify({"message": "Grafo inicializado desde S3.", "nodes": len(all_words)})

    except Exception as e:
        return jsonify({"error": f"Error al construir el grafo: {str(e)}"}), 500

@app.route("/shortest-path", methods=["GET"])
def get_shortest_path():
    if not is_initialized:
        return jsonify({"error": "Grafo no inicializado. Haz POST a /initialize primero."}), 400
    w1 = request.args.get("word1")
    w2 = request.args.get("word2")
    if not w1 or not w2:
        return jsonify({"error": "Faltan parámetros: word1 y word2."}), 400

    try:
        path = graph.shortest_path(w1, w2)
        return jsonify({"path": [node.word for node in path]})
    except nx.NetworkXNoPath:
        return jsonify({"message": "No se encontró un camino entre las palabras dadas."}), 404
    except Exception as e:
        return jsonify({"error": f"Error al encontrar el camino más corto: {str(e)}"}), 500

@app.route("/clusters", methods=["GET"])
def get_clusters():
    if not is_initialized:
        return jsonify({"error": "Grafo no inicializado. Haz POST a /initialize primero."}), 400
    try:
        clusters = graph.clusters()
        cluster_list = [list(cluster) for cluster in clusters]
        return jsonify({"clusters": cluster_list})
    except Exception as e:
        return jsonify({"error": f"Error al obtener clusters: {str(e)}"}), 500

@app.route("/high-connectivity", methods=["GET"])
def get_high_connectivity():
    if not is_initialized:
        return jsonify({"error": "Grafo no inicializado. Haz POST a /initialize primero."}), 400
    degree = request.args.get("degree", 2, type=int)
    try:
        nodes = graph.high_connectivity_nodes(degree)
        return jsonify({"nodes": [n.word for n in nodes]})
    except Exception as e:
        return jsonify({"error": f"Error al obtener nodos de alta conectividad: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
