#-*- coding:utf-8 -*-
try:
	from flask import Flask, render_template, flash, redirect, url_for, request, session, logging , send_from_directory, send_file
	import random, datetime, re
	import json_db, HTML_Forms, app_functions
	import quiz
except Exception as e:
	with open("log.log", 'w') as file:
		file.write(str(e))
	print("[x] Error import: {}".format(e))

# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #

# Application
app = Flask(__name__)
app.secret_key = "SoftwareDieburg_P!nD@t@_{}".format(random.randint(1000000, 9999999))

# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #

# MAIN FLASK PAGES
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #

@app.route('/', methods=["GET", "POST"])
def home():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()

	return render_template("home.html", form=form, json_data=json_data)
# ----------------------------------------------------------------------------------------- #

@app.route('/quiz_loby', methods=["GET", "POST"])
def quiz_lobby():
    form = HTML_Forms.Form(request.form)
    json_data = json_db.read()

    if "lobbys" not in json_data:
        json_data["lobbys"] = {}
    
    if request.method == "POST":
        nickname = str(form.nickname.data)
        session["nickname"] = nickname
        if "users" not in json_data:
            json_data["users"] = {}
        if nickname not in json_data["users"]:
            json_data["users"][nickname] = {}

    json_db.write(json_data)
    return render_template("quiz_lobby.html", form=form, json_data=json_data)

# ----------------------------------------------------------------------------------------- #

@app.route('/quiz_create_new_lobby', methods=["GET", "POST"])
def quiz_create_new_lobby():
    form = HTML_Forms.Form(request.form)
    json_data = json_db.read()

    if request.method == "POST":
        title = form.quiz_title.data

    return render_template("quiz_create_new_lobby.html", form=form, json_data=json_data)

# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #

# App run
if __name__ == "__main__":
	#ipAddress = socket.gethostbyname(socket.gethostname())
	ipAddress = "0.0.0.0"
	app.run(host=ipAddress, port=5002, debug=True)
