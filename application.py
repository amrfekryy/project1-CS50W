import os

from flask import Flask, session, render_template, redirect, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
	if not session.get("user_id"):
		return redirect(url_for("login"))
	return render_template("index.html", username=session["username"])

@app.route("/login", methods=["GET", "POST"])
def login():
	# if login form is submitted
	if request.method == "POST":
		# GET INPUTS
		username = request.form.get("username")
		password = request.form.get("password")

		# TEST INPUTS
		if not username or not password:
			return "One or more field is missing! Please try again"

		user_exists = db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).rowcount
		if not user_exists:
			return "username doesn't exist!"
			
		user_info = db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).fetchone()
		if not check_password_hash(user_info.password, password):
			return "password is not correct!"
		
		# COOKIE USER
		session["user_id"] = user_info.id
		session["username"] = user_info.username

		return redirect(url_for("index"))

	# if login form is requested
	else:	
		return render_template("login.html")

@app.route("/logout")
def logout():
	"""Log user out"""

	# Forget any user_id
	session.clear()
	# Redirect user to login form
	return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
	# if registration form is submitted
	if request.method == "POST":
		# GET INPUTS
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		password2 = request.form.get("password2")

		# TEST INPUTS
		# check all values are provided
		if not username or not email or not password or not password2:
			return "One or more field is missing! Please try again"
		# check passwords match
		if password != password2:
			return "Passwords don't match! Please try again"
		# check username and email are unique
		username_repeated = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount
		email_repeated = db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).rowcount
		if username_repeated:
			return "username already exists!"
		if email_repeated:
			return "email already exists!"
		
		# HASH PASSWORD
		password = generate_password_hash(password)

		# ADD USER
		try:
			db.execute("""INSERT INTO users (username, email, password)
						  VALUES (:username, :email, :password)""",
						  {"username":username, "email":email, "password":password})
			db.commit()
		except:
			return "Failure"
		
		# COOKIE USER
		user_info = db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).fetchone()
		session["user_id"] = user_info.id
		session["username"] = user_info.username

		return redirect(url_for("index"))

	# if registration form is requested
	else:
		return render_template("register.html")

@app.route("/search")
def search():
	# get search text
	q1 = request.args.get("q")
	if not q1:
		return "Search field is empty!"
	# make it partial
	q2 = f"%{q1}%"
	
	# query database enabling case-insensitivity
	book_list = db.execute("""SELECT * FROM books 
		WHERE CONCAT(LOWER(isbn), LOWER(title), LOWER(author), year::text) LIKE LOWER(:q2)""", {"q2":q2}).fetchall()
	# also see COLLATE utf8_general_ci
	
	return render_template("index.html", q1=q1, book_list=book_list, username=session["username"])

