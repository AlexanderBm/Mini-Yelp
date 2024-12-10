from flask import Blueprint, jsonify, request, render_template
from .services import get_reviews_service, write_review_service, get_restaurants_from_db_service, update_restaurants_service

app = Blueprint('app', __name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    restaurant_name = request.args.get('restaurant')
    if not restaurant_name:
        return jsonify({"error": "Restaurant name is required"}), 400
    
    return get_reviews_service(restaurant_name)

@app.route('/write_review', methods=['POST'])
def write_review():
    data = request.json
    restaurant = data.get('restaurant')
    rating = data.get('rating')
    review = data.get('review')
    
    if not restaurant or not isinstance(rating, (int, float)) or not review:
        return jsonify({"error": "Invalid input"}), 400
    
    return write_review_service(restaurant, rating, review)

@app.route('/get_restaurants_from_db', methods=['GET'])
def get_restaurants_from_db():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Location is required"}), 400

    return get_restaurants_from_db_service(location)

@app.route('/update_restaurants', methods=['POST'])
def update_restaurants():
    data = request.json
    location = data.get('location')
    if not location:
        return jsonify({"error": "Location is required"}), 400

    return update_restaurants_service(location)