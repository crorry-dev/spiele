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

# ----------------------------------------------------------------------------------------- #

@app.route('/busfahren_start', methods=["GET", "POST"])
def busfahren_start():
	json_busfahren = json_db.read("busfahren")
	
	session["busfahren_status"] = False

	if "round" not in json_busfahren:
		json_busfahren["round"] = 1
		class_busfahren = busfahren.Busfahren(len(json_busfahren["players"]))
		json_busfahren["map"] = class_busfahren.get_map()
		
		max_round = 0
		for i, _ in enumerate(json_busfahren["map"]):
			for _ in json_busfahren["map"][i]:
				max_round += 1
		json_busfahren["max-round"] = max_round
		for player in json_busfahren["players"]:
			json_busfahren[player] =  class_busfahren.get_player_cards()
			if "status" not in json_busfahren:
				json_busfahren["status"] = {}
			json_busfahren["status"][player] = False
		json_db.write(json_busfahren, "busfahren")
	
	return redirect(url_for("page_busfahren"))

# ----------------------------------------------------------------------------------------- #

@app.route('/busfahren', methods=["GET", "POST"])
def page_busfahren():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()
	json_busfahren = json_db.read("busfahren")

	if "nickname" not in session:
		return redirect(url_for("busfahren_stop"))

	if request.method == "POST":
		session["busfahren_status"] = True
		json_busfahren["status"][session["nickname"]] = True

	check_var = len(json_busfahren["players"])
	for p in range(0, len(json_busfahren["players"])):
		if json_busfahren["status"][json_busfahren["players"][p]]:
			check_var -= 1

	if check_var == 0:
		json_busfahren["round"] += 1
		for p in range(0, len(json_busfahren["players"])):
			json_busfahren["status"][json_busfahren["players"][p]] = False

	if json_busfahren["round"] > json_busfahren["max-round"]:
		anz_cards = []
		for p in json_busfahren["players"]:
			anz_cards.append([p, len(json_busfahren[p])])
		
		anz_player_cards = app_functions.sortListInList(anz_cards, 1)
		# wenn die Letzten gleich sind = random
		looser = anz_cards[-1][0]
		
		json_busfahren["final-looser"] = looser
		json_db.write(json_busfahren, "busfahren")

		if session["nickname"] != looser:
			flash("Das Spiel ist vorbei! {} musst Busfahren".format(looser), "success")
		else:
			flash("Das Spiel ist vorbei! DU musst Busfahren... Viel Erfolg ;) ", "danger")
		return redirect(url_for("page_busfahren_final", _guess="None"))

	json_db.write(json_busfahren, "busfahren")
	return render_template("busfahren.html", form=form, josn_data=json_data, json_busfahren=json_busfahren, check_var=check_var)

# ----------------------------------------------------------------------------------------- #

@app.route('/card/<card>', methods=["GET", "POST"])
def card(card):
	json_busfahren = json_db.read("busfahren")
	if "cards-used" not in json_busfahren:
		json_busfahren["cards-used"] = {}
	if session["nickname"] not in json_busfahren["cards-used"]:
		json_busfahren["cards-used"][session["nickname"]] = []
	
	card_index = 0
	row_index = 0
	round_index = 0
	for r_index,row in enumerate(json_busfahren["map"]):
		row_index += 1
		card_index = 0
		for c in json_busfahren["map"][r_index]:
			card_index += 1
			round_index += 1
			if round_index >= json_busfahren["round"]:
				break
		else:
			continue
		break
	
	if json_busfahren[session["nickname"]][int(card)][0] == json_busfahren["map"][row_index-1][card_index-1][0]:
		if "timeline" not in json_busfahren:
			json_busfahren["timeline"] = []
		json_busfahren["timeline"].append([session["nickname"], json_busfahren[session["nickname"]][int(card)][0], json_busfahren["round"]])
		json_busfahren["cards-used"][session["nickname"]].append(json_busfahren[session["nickname"]][int(card)])
		del json_busfahren[session["nickname"]][int(card)]
		json_db.write(json_busfahren, "busfahren")
		flash("Sie haben die Karte abgelegt, verteilen Sie nun mündlich die schlücke", "success")
	return redirect(url_for("page_busfahren"))

# ----------------------------------------------------------------------------------------- #

@app.route('/busfahren_lobby', methods=["GET", "POST"])
def page_busfahren_lobby():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()
	json_busfahren = json_db.read("busfahren")
	
	if "players" in json_busfahren:
		anz_players = len(json_busfahren["players"])
	elif "nickname" in session and "round" in json_busfahren:
		return redirect(url_for("page_busfahren"))
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
		else:
			nickname = session["nickname"]
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

# ----------------------------------------------------------------------------------------- #

@app.route('/busfahren_final/<string:_guess>', methods=["GET", "POST"])
def page_busfahren_final(_guess):
	form = HTML_Forms.Form(request.form)
	json_busfahren = json_db.read("busfahren")
	global class_busfahren

	if "final-timeline" not in json_busfahren:
		json_busfahren["final-timeline"] = []
	if "final-sips-added" not in json_busfahren:
		json_busfahren["final-sips-added"] = 0

	if "final-cards" not in json_busfahren:
		print("__init__")
		class_busfahren = busfahren.Busfahren(len(json_busfahren["players"]))
		json_busfahren["final-cards"] = class_busfahren.play_final(init=True)
		json_busfahren["final-card-index"] = 0
		json_db.write(json_busfahren, "busfahren")
		return render_template("busfahren_final.html", json_busfahren=json_busfahren)

	if _guess != None and _guess != "" and _guess != "None":
		
		data = class_busfahren.play_final(guess=_guess, cards=json_busfahren["final-cards"])
		print(data)
		if data[0] != 0:
			json_busfahren["final-card-index"] += 1
		else:
			json_busfahren["final-sips-added"] += json_busfahren["final-card-index"] + 1
			json_busfahren["final-cards"] = data[1]
			json_busfahren["final-cards"] = data[1]

	json_db.write(json_busfahren, "busfahren")

	return render_template("busfahren_final.html", json_busfahren=json_busfahren)

# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #

# App run
if __name__ == "__main__":
	#ipAddress = socket.gethostbyname(socket.gethostname())
	ipAddress = "0.0.0.0"
	app.run(host=ipAddress, port=5555, debug=True)