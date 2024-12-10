import sqlite3
from flask import g, jsonify
from threading import Thread
import googlemaps
import os
import re

DATABASES = {
    'restaurants': 'instance/restaurants.db',
    'reviews': 'instance/reviews.db'
}

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

def get_db(db_name):
    db = getattr(g, f'_db_{db_name}', None)
    if db is None:
        db = sqlite3.connect(DATABASES[db_name])
        db.row_factory = sqlite3.Row
        setattr(g, f'_db_{db_name}', db)
    return db

def close_db(error):
    for db_name in DATABASES:
        db = getattr(g, f'_db_{db_name}', None)
        if db is not None:
            db.close()

def get_reviews_service(restaurant_name):
    try:
        conn_restaurants = get_db('restaurants')
        cursor_restaurants = conn_restaurants.cursor()

        cursor_restaurants.execute("SELECT id FROM restaurants WHERE name = ?", (restaurant_name,))
        restaurant = cursor_restaurants.fetchone()

        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404

        restaurant_id = restaurant[0]

        conn_reviews = get_db('reviews')
        cursor_reviews = conn_reviews.cursor()

        cursor_reviews.execute(
            "SELECT review_text, rating, review_date FROM reviews WHERE restaurant_id = ?",
            (restaurant_id,)
        )
        reviews = cursor_reviews.fetchall()

        if not reviews:
            return jsonify({"message": "No reviews yet"}), 200

        formatted_reviews = [
            {"review_text": review["review_text"], "rating": review["rating"], "review_date": review["review_date"]}
            for review in reviews
        ]

        return jsonify(formatted_reviews), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def write_review_service(restaurant, rating, review):
    try:
        rating = max(0, min(5, round(rating, 1)))

        conn_restaurants = get_db('restaurants')
        cursor_restaurants = conn_restaurants.cursor()

        cursor_restaurants.execute("SELECT id FROM restaurants WHERE name = ?", (restaurant,))
        restaurant_record = cursor_restaurants.fetchone()

        if not restaurant_record:
            return jsonify({"error": "Restaurant not found"}), 404

        restaurant_id = restaurant_record[0]

        conn_reviews = get_db('reviews')
        cursor_reviews = conn_reviews.cursor()

        cursor_reviews.execute(
            "INSERT INTO reviews (restaurant_id, review_text, rating) VALUES (?, ?, ?)",
            (restaurant_id, review, rating)
        )

        conn_reviews.commit()

        return jsonify({"message": "Review added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_restaurants_from_db_service(location):
    lat, lng = map(float, location.split(','))
    radius_km = 10 * 1.60934

    try:
        conn_restaurants = get_db('restaurants')
        cursor_restaurants = conn_restaurants.cursor()

        cursor_restaurants.execute("ATTACH DATABASE ? AS reviews_db", (DATABASES['reviews'],))
        
        cursor_restaurants.execute("""
            SELECT r.name, IFNULL(AVG(rv.rating), 0) AS avg_rating
            FROM restaurants r
            LEFT JOIN reviews rv ON r.id = rv.restaurant_id
            WHERE (6371 * acos(
                cos(radians(?)) * cos(radians(r.latitude)) * 
                cos(radians(r.longitude) - radians(?)) + 
                sin(radians(?)) * sin(radians(r.latitude))
            )) <= ?
            GROUP BY r.id
        """, (lat, lng, lat, radius_km))

        restaurants = [
            {"name": row["name"], "avg_rating": round(row["avg_rating"], 1)}
            for row in cursor_restaurants.fetchall()
        ]

        return jsonify(restaurants)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_restaurants_service(location):
    lat, lng = map(float, location.split(','))

    def fetch_and_update():
        try:
            new_restaurants = get_restaurants((lat, lng))

            conn_restaurants = get_db('restaurants')
            cursor_restaurants = conn_restaurants.cursor()

            for res, res_lat, res_lng in new_restaurants:
                normalized_name = replace_single_quotes(res)
                cursor_restaurants.execute(
                    "SELECT id FROM restaurants WHERE name = ? AND latitude = ? AND longitude = ?",
                    (normalized_name, res_lat, res_lng)
                )
                if not cursor_restaurants.fetchone():
                    cursor_restaurants.execute(
                        "INSERT INTO restaurants (name, latitude, longitude) VALUES (?, ?, ?)",
                        (normalized_name, res_lat, res_lng)
                    )
                    conn_restaurants.commit()
        except Exception as e:
            print(f"Error in background task: {e}")

    Thread(target=fetch_and_update).start()
    return jsonify({"message": "Update started"}), 202

def get_restaurants(location):
    map_client = googlemaps.Client(GOOGLE_API_KEY)
    
    search_string = 'restaurant'
    distance = 16093.4
    restaurant_list = []

    response = map_client.places_nearby(
        location=location,
        keyword=search_string,
        radius=distance)

    restaurant_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')

    while next_page_token:
        response = map_client.places_nearby(
            location=location,
            keyword=search_string,
            radius=distance,
            page_token=next_page_token)
        restaurant_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token')

    restaurants = []
    for restaurant in restaurant_list:
        name = restaurant.get("name")
        location = restaurant.get("geometry", {}).get("location", {})
        lat = location.get("lat")
        lng = location.get("lng")
        restaurants.append([name, lat, lng])
    return restaurants

def replace_single_quotes(text):
    return re.sub(r"'", '’', text)