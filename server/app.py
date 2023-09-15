#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_dict = []
    for bakery in bakeries:
        bakeries_dict.append(bakery.to_dict())
    
    response = make_response(jsonify(bakeries_dict),200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(jsonify(bakery_dict), 200)
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price).all()
    goods_dict = []
    for good in goods:
        goods_dict.append(good.to_dict())
    response = make_response(jsonify(goods_dict),200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    good_dict = good.to_dict()
    response = make_response(jsonify(good_dict),200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
