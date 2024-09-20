from flask import Flask, jsonify, request, render_template
import json
import requests
import time
import googlemaps

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    restaurant = request.args.get('restaurant')

    with open('reviews.json', 'r') as file:
        reviews = json.load(file)
        
    try:
        return jsonify(reviews[restaurant][1:])
    except Exception as e:
        return jsonify("No reviews yet")

@app.route('/write_review', methods=['POST'])
def write_review():
    data = request.json
    restaurant = data.get('restaurant')
    rating = data.get('rating')
    review = data.get('review')

    with open('reviews.json', 'r') as file:
        reviews = json.load(file)
    
    rating = 5 if rating > 5 else round(rating, 1)
    rating = 0 if rating < 0 else round(rating, 1)
    if restaurant in reviews:
        rev_res = reviews[restaurant]
        rev_res[0] = round((rev_res[0] * (len(rev_res) - 1) + rating) / len(rev_res), 1)
        reviews[restaurant].append([rating, review])
    else:
        reviews[restaurant] = [rating, [rating, review]]
    
    with open('reviews.json', 'w') as f: 
        json.dump(reviews, f)

@app.route('/get_restaurants', methods=['GET'])
def get_average_ratings_and_restaurants_nearby():
    location = request.args.get('location')
    if location:
        lat, lng = map(float, location.split(','))
    else:
        return jsonify({"error": "Location not provided"}), 400

    location = (lat, lng)
    list_of_restaurants = get_restaurants(location)

    with open('reviews.json', 'r') as file:
        reviews = json.load(file)
    
    res_and_rating = []
    for res in list_of_restaurants:
        if res in reviews:
            res_and_rating.append([res, reviews[res][0]])
        else:
            res_and_rating.append([res, 0])
    
    return jsonify(res_and_rating)

def get_restaurants(location):
    GOOGLE_API_KEY = 'AIzaSyCYn-VKpAOnP66lc_GrbWQ1XF_opF5kT5I'
    map_client = googlemaps.Client(GOOGLE_API_KEY) 
    
    search_string = 'restaurant'
    distance = 8046.72
    restaurant_list = []
    
    response = map_client.places_nearby(
        location=location,
        keyword=search_string,
        radius=distance)
    
    restaurant_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')

    while next_page_token:
        time.sleep(2)
        response = map_client.places_nearby(
            location=location,
            keyword=search_string,
            radius=distance,
            page_token = next_page_token)
        restaurant_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token')
        
    return [item['name'] for item in restaurant_list]

if __name__ == '__main__':
    app.run(debug=True)