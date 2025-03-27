from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (pretend this is a database)
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]

# GET all items
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({"items": items}), 200

# GET a single item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify({"item": item}), 200
    return jsonify({"error": "Item not found"}), 404

# POST to add a new item
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    new_id = max(item["id"] for item in items) + 1 if items else 1
    new_item = {"id": new_id, "name": data["name"]}
    items.append(new_item)
    return jsonify({"item": new_item}), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
