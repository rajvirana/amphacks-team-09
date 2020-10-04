import os

from flask import Flask, session, render_template, request
from flask_session import Session
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests



app = Flask(__name__)
Bootstrap(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
# if not os.getenv("KEY"):
#     raise RuntimeError("Goodreads API is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

if __name__ == '__main__':
    app.run()

@app.route("/")
def index():
    return render_template("entry.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login_request", methods=["POST"])
def login_request():
    username = request.form.get("username")
    password = request.form.get("password")

    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
        return render_template("error.html", message="No such user with that id.")
    if db.execute("SELECT * FROM users WHERE (username = :username) AND (password = :password)", {"username": username, "password": password}).rowcount==1:
        return render_template("search.html")
    return render_template("error.html", message="incorrect login info")

@app.route("/signup_request", methods=["POST"])
def signup_request():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    username = request.form.get("username")
    password = request.form.get("password")

    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 1:
        return render_template("entry.html", message="[ ! ] User already exists. Try logging in.")
    db.execute("INSERT INTO users (username, password, firstname, lastname) VALUES (:username, :password, :firstname, :lastname)",
               {"username": username, "password": password, "firstname": firstname, "lastname": lastname})
    db.commit()
    return render_template("search.html")

@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/search/query", methods=["POST"])
def search_request():
    q = request.form.get("query")

    result = db.execute("SELECT * FROM books WHERE LOWER(isbn) LIKE LOWER('%" + q + "%') OR LOWER(title) LIKE LOWER('%" +
               q + "%') OR LOWER(author) LIKE LOWER('%" + q + "%') LIMIT 20").fetchall()
    if len(result) == 0:
        message = "Sorry, no search results found for "
    else:
        message = "Displaying returned results for "
    return render_template("search.html", results=result, message=message, query=q)


@app.route("/search/<string:isbn>")
def search_result(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": str(isbn)}).fetchone()

    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                    params={"key": os.environ['KEY'], "isbns": isbn})
    print(res.json())
    result = res.json()
    rating_details = {
        "average_rating": result['books'][0]['average_rating'],
        "number_ratings": result['books'][0]['ratings_count'],
        "number_reviews": result['books'][0]['reviews_count'],
        "book_id" : result['books'][0]['id'],
    }

    reviews = requests.get("https://www.goodreads.com/book/show.json",
                               params={"key": os.environ['KEY'],"id":rating_details['book_id']})

    temp_result = reviews.json()
    review_widget = temp_result['reviews_widget']
    return render_template("searchresult.html", book=book, results=rating_details, reviews=review_widget)


    #except:
    #   print("entered exception")
    #   return render_template("error.html", message="Sorry, no reviews available for this book.")




@app.route("/review")
def review_result():

    return render_template("reviewresult.html")



