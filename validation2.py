@app.route("/login", methods=["GET", "POST"])
def login():
	# if login form is submitted
	if request.method == "POST":
		# GET INPUTS
		username = request.form.get("username")
		password = request.form.get("password")

		# TEST INPUTS
		# if not username or not password:
		# 	return "One or more field is missing! Please try again"
		# (checked on frontend)

		global login_check

		user_exists = db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).rowcount
		if not user_exists:
			# return "username doesn't exist!"
			# return render_template("login.html", not_user=True)

			login_check = {"user":False}
		else:
			user_info = db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).fetchone()
			if not check_password_hash(user_info.password, password):
				# return "password is not correct!"
				# return render_template("login.html", wrong_password=True)

				login_check = {"user":True, "password":False}
			else:
				# COOKIE USER
				session["user_id"] = user_info.id
				session["username"] = user_info.username

				login_check = {"user":True, "password":True}
		
		validation("login")

		return redirect(url_for("index"))

	# if login form is requested
	else:	
		return render_template("login.html")

@app.route("/validation/<string:form>")
def validation(form):
	if form == "login":
		return jsonify(login_check)


# in script.js:

# // Replace ./data.json with your JSON feed
# fetch("/validation/login").then(response => {
#   return response.json();
# }).then(data => {
#   // Work with JSON data here
#   if (!data.user)
#   {
#     alert("user name doesn't exist");
#     return false;
#   }
# }).catch(err => {
#   // Do something for an error here
# });
