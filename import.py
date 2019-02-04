import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# check for DATABASE_URL environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
# set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	# import data from "books.csv" into "books" table
	with open("books.csv") as file:
		reader = csv.reader(file)
		i = 0
		for isbn, title, author, year in reader:
			db.execute("INSERT INTO books (isbn, title, author, year) VALUES ( :isbn, :title, :author, :year)", 
				{"isbn":isbn, "title":title, "author":author, "year":year})
			# see importing progress
			i += 1
			print(i)
		db.commit()

if __name__ == "__main__":
	main()
