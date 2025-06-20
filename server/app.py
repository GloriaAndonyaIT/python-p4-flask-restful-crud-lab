#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Plant Store API</h1>'

# GET route to fetch all plants
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200

# GET route to fetch a single plant
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return jsonify(plant.to_dict()), 200

# POST route to create a new plant
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    
    new_plant = Plant(
        name=data.get('name'),
        image=data.get('image'),
        price=data.get('price'),
        is_in_stock=data.get('is_in_stock', True)
    )
    
    db.session.add(new_plant)
    db.session.commit()
    
    return jsonify(new_plant.to_dict()), 201

# PATCH route to update an existing plant
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get_or_404(id)
    
    data = request.get_json()
    
    # Update the plant's attributes based on what's provided
    if 'name' in data:
        plant.name = data['name']
    if 'image' in data:
        plant.image = data['image']
    if 'price' in data:
        plant.price = data['price']
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    
    db.session.commit()
    
    return jsonify(plant.to_dict()), 200

# DELETE route to remove a plant
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get_or_404(id)
    
    db.session.delete(plant)
    db.session.commit()
    
    # Return empty response with 204 status code
    return '', 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)