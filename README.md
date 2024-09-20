# Mini Yelp Clone

## Overview

The Mini Yelp Clone is a web application that allows users to discover nearby restaurants and leave reviews. It utilizes the Google Maps API to fetch restaurant information based on the user's geolocation. The app stores reviews in a JSON file, providing an easy way for users to see average ratings and read or submit reviews.

## Features

- **Restaurant Discovery**: Automatically retrieves nearby restaurants based on the user's location.
- **Reviews**: Users can view existing reviews and submit their own ratings and comments.
- **Average Ratings**: Displays the average rating for each restaurant based on user submissions.
- **Responsive Design**: Optimized for desktop and mobile views.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with Flask
- **Database**: JSON file (`reviews.json`)
- **API Integration**: Google Maps API for restaurant data

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask
- Google Maps API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mini-yelp-clone
   ```

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
     ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the App**: Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- **Homepage**: The homepage will display a list of nearby restaurants based on your current location. Click on a restaurant name to view its reviews.
- **Review Page**: On the review page, you can see existing reviews and submit your own by entering a rating and review text.

## File Structure

```
/mini-yelp-clone
│
├── app.py               # Main Flask application
├── reviews.json         # JSON file to store reviews
└── templates
    ├── index.html       # Homepage template
    └── reviews.html     # Reviews page template
```
