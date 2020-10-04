import os

from flask import Flask, session, render_template, request
from flask_session import Session
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from random import randrange

import requests



app = Flask(__name__)
Bootstrap(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
<<<<<<< HEAD
    raise RuntimeError("DATABASE_URL is not set")
# if not os.getenv("KEY"):
#     raise RuntimeError("Goodreads API is not set")
=======
    raise RuntimeError("DB URL is not set")

#if not os.getenv("KEY"):
#    raise RuntimeError("API is not set")
>>>>>>> 01a11caaa5faa099654ecba58e3212ccc22c8d1c

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


#set up session variables

def random():
    session = {}
    print(randrange(1000))
    session["number"] = int(randrange(0,1000))
    return None




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
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")

    if db.execute("SELECT * FROM volunteer WHERE first_name = :firstName", {"firstName": firstName}).rowcount == 0:
        return render_template("error.html", message="No such user with that id.")

    if db.execute("SELECT * FROM volunteer WHERE (first_name = :firstName) AND (last_name = :lastName)", {"firstName": firstName, "lastName": lastName}).rowcount==1:
        person = db.execute("SELECT * FROM volunteer WHERE (first_name = :firstName) AND (last_name = :lastName)",
                   {"firstName": firstName, "lastName": lastName}).fetchall()
        random()
        session["firstName"] = firstName
        session["lastName"] = lastName
        session["user_id"] = person[0][1]

        # want to find all postings with logged in user as the author_id
        # want to join all
        results = db.execute("SELECT * FROM postings WHERE (author_id = :author_id)",
                   {"author_id": 742}).fetchall()


        print(results)
        return render_template("search.html", results=results)
    return render_template("error.html", message="incorrect login info")

@app.route("/login_request", methods=["POST"])
def my_matches():

    if db.execute("SELECT * FROM volunteer WHERE (first_name = :firstName) AND (last_name = :lastName)", {"firstName": firstName, "lastName": lastName}).rowcount==1:
        person = db.execute("SELECT * FROM volunteer WHERE (first_name = :firstName) AND (last_name = :lastName)",
                   {"firstName": firstName, "lastName": lastName}).fetchall()


        print(person[0][1])
        results = db.execute("SELECT * FROM postings WHERE (author_id = :author_id)",
                   {"author_id": person[0][1]}).fetchall()
        print(results)
        return render_template("search.html")
    return render_template("error.html", message="incorrect login info")



@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/newpost")
def new_post():
    return render_template("newpost.html")

@app.route("/search")
def confirm():
    return render_template("search.html")


@app.route("/search")
def delete():
    return render_template("search.html")