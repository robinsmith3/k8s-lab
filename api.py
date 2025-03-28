from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://api_user:securepassword123@postgres-service:5432/flask_api_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = 'items'
    __table_args__ = {'schema': 'public'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

def init_db():
    logger.info("Starting init_db")
    logger.info(f"Connecting to: {app.config['SQLALCHEMY_DATABASE_URI']}")
    for _ in range(5):
        try:
            with app.app_context():
                logger.info("Attempting to create tables")
                db.create_all()
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names(schema='public')
                logger.info(f"Tables in public schema: {tables}")
                if 'items' in tables:
                    logger.info("Tables created successfully")
                else:
                    logger.error("Items table not found after create_all")
            break
        except Exception as e:
            logger.error(f"Failed to connect to DB: {e}")
            time.sleep(5)
    else:
        raise Exception("Could not initialize database after retries")

logger.info("Before init_db")
init_db()
logger.info("After init_db")

@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify({
        "message": "List of available items",
        "items": [item.to_dict() for item in items]
    }), 200

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify({"item": item.to_dict()}), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    new_item = Item(name=data["name"])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"item": new_item.to_dict()}), 201

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            "message": f"Item {item_id} deleted successfully. Use GET /api/items to see the updated list."
        }), 200
    return jsonify({
        "error": "Item not found",
        "hint": "Use GET /api/items to see available items first."
    }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)