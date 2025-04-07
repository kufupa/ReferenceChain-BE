from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
from src.TreeGeneration.treegen import build_reg_tree, explore_new_node
from src.Models.articlenode import ArticleNode

app = Flask("Causalitree")
CORS(app)  # Allow requests from the frontend

roots = []

@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = "script-src 'self' 'nonce-diddy'"
    return response

@app.route('/api/start', methods=['POST'])
def index_page():
    print("DEBUG: index_page called")
    data = request.get_json()
    if not data:
        print("DEBUG: index_page - no JSON received")
        return jsonify({"error": "No JSON received"}), 400
    
    url_from_request = data.get('url')
    print("DEBUG: index_page received url:", url_from_request)

    if url_from_request == r"http://localhost:3000/":
        print("DEBUG: index_page - localhost request")
        print("We here boys")
        return jsonify({"message": "ok"}), 200

    explore_new_node(url_from_request, roots)
    print("DEBUG: index_page - completed explore_new_node")

@app.route('/api/start', methods=['GET'])
def start():
    print("DEBUG: start called")
    if len(roots) == 0:
        print("DEBUG: start - no roots available")
        return jsonify({"error": "Not yet ready"}), 500
    data = {"nodes": [roots[-1].to_client()]}
    print("DEBUG: start - returning nodes data")
    return jsonify(data), 200

@app.route('/api/prevents', methods=['GET'])
def get_prevents():
    print("DEBUG: get_prevents called")
    query = request.args.get('url')
    print("DEBUG: get_prevents received query:", query)
    predecessors = roots[-1].find_predecessors_2(query)
    combined = {"nodes": []}
    for node in predecessors:
        print("DEBUG: get_prevents processing node", node)
        combined["nodes"].append(node.to_client())
        thread = threading.Thread(target=node.get_new_preds)
        thread.start()
        print("DEBUG: get_prevents - started thread for node")

    print("DEBUG: get_prevents completed")
    return jsonify(combined), 200

@app.route('/api/explore-future', methods=['GET'])
def explore_future():
    print("DEBUG: explore_future called")
    if len(roots) == 0:
        print("DEBUG: explore_future - no roots available")
        return jsonify({"error": "No JSON received"}), 400
    future = roots[-1].get_potential_future()
    print("DEBUG: explore_future - future data:", future)
    return jsonify({"future": future}), 200

@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    print("DEBUG: get_nodes called")
    if len(roots) == 0:
        print("DEBUG: get_nodes - no roots available")
        return jsonify({"error": "No JSON received"}), 400
    if roots[0].title is None and len(roots[0].predecessors) > 0:
        print("DEBUG: get_nodes - fixing root")
        newRoot = roots[0].predecessors[0]
        newRoot.sucessors = []
        roots[0] = newRoot
    
    combined = {"nodes": []}
    
    queue = [roots[-1]]

    while len(queue) > 0:
        node = queue.pop()
        print("DEBUG: get_nodes - processing node", node)
        combined["nodes"].append(node.to_client())
        queue += node.predecessors

    print("DEBUG: get_nodes - completed, returning nodes data")
    return jsonify(combined), 200


@app.route('/api/nodes', methods=['POST'])
def explore_url():
    print("DEBUG: explore_url called")
    data = request.get_json()
    if not data:
        print("DEBUG: explore_url - no JSON received")
        return jsonify({"error": "No JSON received"}), 400
    
    url_from_request = data.get('url')
    print("DEBUG: explore_url received url:", url_from_request)

    explore_new_node(url_from_request, roots)
    print("DEBUG: explore_url - completed explore_new_node")

    return jsonify({"message": "Data received", "data": data}), 200

if __name__ == '__main__':
    print("DEBUG: Starting Flask app")
    app.run(debug=True)