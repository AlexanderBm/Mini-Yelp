import json
import requests
import time
import pandas as pd
import googlemaps

def get_reviews(restaurant):
    with open('reviews.json', 'r') as file:
        reviews = json.load(file)
        
    try:
        return reviews[restaurant][1:]
    except Exception as e:
        return "No reviews yet"
    
def write_review(restaurant, rating, review):
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

def get_average_ratings(list_of_restaurants):
    with open('reviews.json', 'r') as file:
        reviews = json.load(file)
    
    res_and_rating = []
    for res in list_of_restaurants:
        if res in reviews:
            res_and_rating.append([res, reviews[res][0]])
        else:
            res_and_rating.append([res, 0])
    
    return res_and_rating

def get_restaurants(location):
    # map_client = googlemaps.Client(GOOGLE_API_KEY) 
    
    search_string = 'restaurant'
    distance = 8046.72
    restaurant_list = []
    
    response = map_client.places_nearby(
        location=location,
        keyword=search_string,
        radius=distance
    )
    
    restaurant_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')

    while next_page_token:
        time.sleep(2)
        response = map_client.places_nearby(
            location=location,
            keyword=search_string,
            radius=distance,
            page_token = next_page_token
        )
        restaurant_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token')
        
    return [item['name'] for item in restaurant_list]