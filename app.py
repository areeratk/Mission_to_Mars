from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    print(listings)
    return render_template("index.html", nasa_scraped_data=listings)


@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings_data = mission_to_mars.scrape()
    listings.update({}, listings_data, upsert=True)
  
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)