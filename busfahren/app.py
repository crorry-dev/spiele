#-*- coding:utf-8 -*-

try:
	from flask import Flask, render_template, flash, redirect, url_for, request, session, logging , send_from_directory, send_file
	import random, datetime, re
	import json_db, HTML_Forms, app_functions
	import busfahren
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
@app.route("/login", methods=["GET","POST"])
def login():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()
	if request.method == "POST":
		email = str(form.login_email.data)
		password = str(form.login_password.data)
		salt = json_data["users"][email]["password_salt"]
		if json_data["users"][email]["password"] == app_functions.password_hash(password, salt)[0]:
			flash("Sie haben sich erfolgreich eingeloggt", "success")
			session["email"] = email
			session["name"] = json_data["users"][email]["firstname"] + " " + json_data["users"][email]["name"]
			return redirect(url_for("home"))
		else:
			flash("Die eingegebenen Nutzerdaten stimmen nicht!", "danger")
			return redirect(url_for("login"))
	

	return render_template("login.html", form=form, json_data=json_data)

# ----------------------------------------------------------------------------------------- #

@app.route("/register", methods=["GET", "POST"])
def register():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()

	if request.method == "POST": 
		firstname = str(form.register_firstname.data)
		name = str(form.register_name.data)
		email = str(form.register_email.data)
		password = str(form.register_password.data)
		confirm_password = str(form.register_confirm_password.data)
		telephone = str(form.register_telephone.data)

		hashed_passwod = app_functions.password_hash(password)

		if firstname != "" and name != "" and email != "" and password != "" and confirm_password != "":
			if "users" not in json_data:
				json_data["users"] = {}
			if email in json_data["users"]:
				flash("Diese Emailadressse ist bereits mit einem Account verknüpft! Wählen Sie Passwort vergessen auf der Login Seite!", "danger")
				return redirect(url_for("register"))
			json_data["users"][email] = {"firstname": firstname, "name": name, "telephone": telephone, "password": hashed_passwod[0], "password_salt": hashed_passwod[1]}
			json_db.write(json_data)
			py_send_mail.send_mail(email, "Registrierung bei Software-Dieburg", "Vielen Dank für Ihre Registrierung bei Software-Dieburg.de!")
			flash("Sie haben Sich erfolgreich ergistriert!", "success")
			return redirect(url_for("login"))
		else:
			flash("Alle Felder müssen ausgefüllt sein außer der Telefonnummer!", "danger")

	return render_template("register.html", form=form, json_data=json_data)

# ----------------------------------------------------------------------------------------- #

@app.route("/login/forgot_password", methods=["GET", "POST"])
def forgot_password():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()

	if request.method == "POST":
		email = str(form.login_email.data)
		if email in json_data["users"]:
			random_password = app_functions.generateRandomPassword()
			hashed_password = app_functions.password_hash(random_password)
			py_send_mail.send_mail(email, "Neues Passwort bei Software-Dieburg", "Ihr neues Passwort lautet:<br><br>{}<br><br>".format(random_password))
			json_data["users"][email]["password"] = hashed_password[0]
			json_data["users"][email]["password_salt"] = hashed_password[1]
			json_db.write(json_data)
			flash("Ihr Passwort wurde zurückgesetzt. Bitte überprüfen Sie Ihre Emails", "success")
			return redirect(url_for("home"))
		else:
			flash("Diese Email ist nicht in unserem System!", "danger")
			return redirect(url_for("home"))
		
	return render_template("forgot_password.html", form=form, json_data=json_data) 

# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #

@app.route('/busfahren_stop', methods=["GET", "POST"])
def busfahren_stop():
	json_busfahren = json_db.read("busfahren")
	session.clear()
	json_busfahren = {}
	json_db.write(json_busfahren, "busfahren")
	return redirect(url_for("home"))

@app.route('/busfahren_start', methods=["GET", "POST"])
def busfahren_start():
	json_busfahren = json_db.read("busfahren")
	
	session["busfahren_status"] = False

	if "round" not in json_busfahren:
		json_busfahren["round"] = 1
		class_busfahren = busfahren.Busfahren(len(json_busfahren["players"]))
		json_busfahren["map"] = class_busfahren.get_map()
		
		for player in json_busfahren["players"]:
			json_busfahren[player] =  class_busfahren.get_player_cards()
			if "status" not in json_busfahren:
				json_busfahren["status"] = {}
			json_busfahren["status"][player] = False
		json_db.write(json_busfahren, "busfahren")
	
	return redirect(url_for("page_busfahren"))

@app.route('/busfahren', methods=["GET", "POST"])
def page_busfahren():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()
	json_busfahren = json_db.read("busfahren")

	if request.method == "POST":
		session["busfahren_status"] = True
		json_busfahren["status"][session["nickname"]] = True

	check_var = len(json_busfahren["players"])
	for p in range(0, len(json_busfahren["players"])):
		if json_busfahren["status"][json_busfahren["players"][p]]:
			print(json_busfahren["status"][json_busfahren["players"][p]])
			check_var -= 1
	if check_var == 0:
		json_busfahren["round"] += 1
		for p in range(0, len(json_busfahren["players"])):
			json_busfahren["status"][json_busfahren["players"][p]] = False

	json_db.write(json_busfahren, "busfahren")
	return render_template("busfahren.html", form=form, josn_data=json_data, json_busfahren=json_busfahren, check_var=check_var)

@app.route('/card/<card>/<string:player>', methods=["GET", "POST"])
def card(card, player):
	json_busfahren = json_db.read("busfahren")
	if "cards-used" not in json_busfahren:
		json_busfahren["cards-used"] = {}
	if player not in json_busfahren["cards-used"]:
		json_busfahren["cards-used"][player] = []
	
	list_card = [int(re.findall(r'\d+', card)[0]), str(re.findall(r'[A-Z]', card)[0])]
	round_cards = []

	for l in json_busfahren["map"][json_busfahren["round"]-1]:
		round_cards.append(l[0])

	if list_card in json_busfahren[player] and list_card[0] in round_cards:
		json_busfahren[player].remove(list_card)
		json_busfahren["cards-used"][player].append(list_card)

		if "timeline" not in json_busfahren:
			json_busfahren["timeline"] = []
		
		json_busfahren["timeline"].append([session["nickname"], list_card[0], json_busfahren["round"]])

		json_db.write(json_busfahren, "busfahren")
		flash("Die Karte wurde gelegt, teile jetzt mündlich mit wer die Schlücke trinken soll!", "success")
	else:
		flash("Diese Karte kann in dieser Runde nicht gelegt werden!", "danger")
	return redirect(url_for("page_busfahren"))

@app.route('/busfahren_lobby', methods=["GET", "POST"])
def page_busfahren_lobby():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()
	json_busfahren = json_db.read("busfahren")
	
	if "players" in json_busfahren:
		anz_players = len(json_busfahren["players"])
	else:
		anz_players = 0

	if request.method == "POST":
		if "nickname" not in session:
			nickname = form.busfahren_nickname.data.split()[0]
			if "players" not in json_busfahren:
				json_busfahren["players"] = []
			if nickname != "" and nickname not in json_busfahren["players"]:
				session["nickname"] = nickname	
				json_busfahren["players"].append(nickname)

				json_db.write(json_busfahren, "busfahren")
			else:
				flash("Dieser Nickname ist bereits vergeben oder der Name ist ungültig", "danger")
		return redirect(url_for("page_busfahren_lobby"))

	return render_template("/busfahren_lobby.html", form=form, josn_data=json_data, anz_players=anz_players, json_busfahren=json_busfahren)










# App run
if __name__ == "__main__":
	#ipAddress = socket.gethostbyname(socket.gethostname())
	ipAddress = "0.0.0.0"
	app.run(host=ipAddress, port=5050, debug=True)