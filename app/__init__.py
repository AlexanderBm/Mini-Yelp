from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('MINI_YELP_SECRET_KEY', 'fallback-secret-key')
    app.config['DATABASES'] = {
        'restaurants': 'instance/restaurants.db',
        'reviews': 'instance/reviews.db'
    }

    from .routes import app as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app