import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://api_user:securepassword123@postgres-service:5432/flask_api_db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://api_user:securepassword123@postgres-service:5432/flask_api_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Item model
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

with app.app_context():
    db.create_all()

# GET all items
@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify({"items": [item.to_dict() for item in items]}), 200

# GET a single item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify({"item": item.to_dict()}), 200
    return jsonify({"error": "Item not found"}), 404

# POST to add a new item
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    new_item = Item(name=data["name"])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"item": new_item.to_dict()}), 201

# Handle /api specifically
@app.route('/api', methods=['GET'])
def api_root():
    return jsonify({"message": "Welcome to the API. Use /api/items to access resources."}), 200

# Catch-all for undefined routes
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    return jsonify({"error": "Not found. Try /api/items instead."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)