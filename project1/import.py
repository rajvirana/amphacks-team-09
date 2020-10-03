import os
import csv
import pandas
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def import_books():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
    #books_list = pandas.read_csv("books.csv", sep=";", delimiter=",", header=0)
    #for i in range(0,5000):
        # the :origin, etc is placeholders where the origin and variables will be placed
        # and the next line provides a dictionary telling what to place in the placeholders above
        db.execute("INSERT INTO books (isbn, title, author, publication_year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title,
                     "author": author, "year": year})
        print(f"Added book with isbn = {isbn}, "
              f"title = {title}, "
              f"author = {author}, "
              f"year = {year}.")
    db.commit()


import_books()