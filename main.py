from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to format neighborhood name for URL
def format_neighborhood(neighborhood):
    return neighborhood.replace(" ", "_")

# Function to scrape and return restaurant information
def scrape_restaurants(neighborhood, cuisine):
    formatted_neighborhood = format_neighborhood(neighborhood)
    url = f"https://www.yelp.com/search?find_desc=restaurants&find_loc=New+York%2C+NY+10001&cflt={cuisine}&open_now=8352&attrs=OutdoorSeating&l=p%3ANY%3ANew_York%3AManhattan%3A{formatted_neighborhood}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        restaurants = soup.find_all("div", class_="arrange__09f24__LDfbs css-1qn0b6x")

        # Create a list to store restaurant names and descriptions
        restaurant_info = []

        for restaurant in restaurants:
            h3 = restaurant.find("h3", class_="css-1agk4wl")
            p = restaurant.find("p", class_="css-16lklrv")
            a = restaurant.find("a", class_="css-19v1rkv")

            if h3 and p and a:
                restaurant_name = h3.text.strip()
                restaurant_description = p.text.strip()
                restaurant_link = a["href"]
                restaurant_info.append((restaurant_name, restaurant_description, restaurant_link))

        return restaurant_info

    else:
        return None

# List of Manhattan neighborhoods
neighborhoods = [
    "Alphabet City",
    "Battery Park",
    "West Village",
    "Yorkville"
]

# Define the home route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_neighborhood = request.form["neighborhood"]
        cuisine_type = request.form["cuisine"]
        restaurant_info = scrape_restaurants(selected_neighborhood, cuisine_type)
        return render_template("index.html", neighborhoods=neighborhoods, selected_neighborhood=selected_neighborhood,
                               cuisine_type=cuisine_type, restaurant_info=restaurant_info)

    return render_template("index.html", neighborhoods=neighborhoods)

if __name__ == "__main__":
    app.run(debug=True)
