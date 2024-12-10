# Mini Yelp

## Overview

The Mini Yelp is a web application that allows users to discover nearby restaurants and leave reviews. It integrates the Google Maps API to fetch restaurant information based on the user's geolocation and stores restaurant and review data in a SQLite database. Users can see average ratings, read reviews, and submit their own.

## Features

- **Restaurant Discovery**: Automatically retrieves nearby restaurants based on the user's location and stores them in a database.
- **Reviews**: Users can view existing reviews and submit their own ratings and comments.
- **Average Ratings**: Displays the average rating for each restaurant based on user submissions.
- **Database-Driven**: Data for restaurants and reviews is stored in SQLite databases for efficient querying and persistence.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with Flask
- **Database**: SQLite (`restaurants.db` and `reviews.db`)
- **API Integration**: Google Maps API for restaurant data

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask
- SQLite
- Google Maps API key
- `python-dotenv` package (optional for environment variable management)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mini-yelp

2. **Install Flask**:
   ```bash
   pip install Flask
   ```

3. **Set up Google Maps API**:
   - Create a Google Cloud account and set up a project.
   - Enable the Google Maps Places API.
   - Obtain your API key and set it as an environment variable:
     ```bash
     export GOOGLE_API_KEY='your_api_key_here'
     export MINI_YELP_SECRET_KEY='your_secret_key_here'
     ```

4. **Run the Application**:
   ```bash
   python run.py
   ```

5. **Access the App**: Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- **Homepage**: The homepage will display a list of nearby restaurants based on your current location. Click on a restaurant name to view its reviews.
- **Review Page**: On the review page, you can see existing reviews and submit your own by entering a rating and review text.

## File Structure

```
mini-yelp/
│
├── app/                         # Application code
│   ├── __init__.py              # Flask app factory
│   ├── routes.py                # Route definitions
│   ├── services.py              # Business logic
│   └── templates/               # HTML templates
│       ├── home.html            # Homepage template
│       └── reviews.html         # Reviews page template
│
├── instance/                    # Contains SQLite database files
│   ├── restaurants.db           # Restaurants database
│   └── reviews.db               # Reviews database
│
├── run.py                       # Entry point to run the app
├── README.md                    # Documentation
```
