#-*- coding:utf-8 -*-
try:
	from flask import Flask, render_template, flash, redirect, url_for, request, session, logging , send_from_directory, send_file
	import random, datetime, re
	import json_db, HTML_Forms, app_functions, py_send_mail
	import py_quiz
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
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #

@app.route("/login", methods=["GET","POST"])
def login():
    form = HTML_Forms.Form(request.form)
    json_data = json_db.read()
    if request.method == "POST":
        email = str(form.login_email.data)
        password = str(form.login_password.data)
        if email not in json_data["page-users"]:
            flash("Diese Email ist uns nicht bekannt!", "danger")
            return redirect(url_for("login"))
        salt = json_data["page-users"][email]["password_salt"]
        if json_data["page-users"][email]["password"] == app_functions.password_hash(password, salt)[0]:
            flash("Sie haben sich erfolgreich eingeloggt", "success")
            session["email"] = email
            session["nickname"] = json_data["page-users"][email]["nickname"]
            #session["name"] = json_data["page-users"][email]["firstname"] + " " + json_data["page-users"][email]["name"]
            return redirect(url_for("quiz_lobby"))
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
        #firstname = str(form.register_firstname.data)
        #name = str(form.register_name.data)
        email = str(form.register_email.data)
        password = str(form.register_password.data)
        confirm_password = str(form.register_confirm_password.data)
        nickname = str(form.register_nickname.data)

        hashed_passwod = app_functions.password_hash(password)

        if nickname != "" and email != "" and password != "" and confirm_password != "":
            if "page-users" not in json_data:
                json_data["page-users"] = {}
            if email in json_data["page-users"]:
                flash("Diese Emailadressse ist bereits mit einem Account verknüpft! Wählen Sie Passwort vergessen auf der Login Seite!", "danger")
                return redirect(url_for("register"))
            json_data["page-users"][email] = {}
            for e in json_data["page-users"]:
                if nickname in json_data["page-users"][e]:
                    flash("Dieser Nickname ist bereits vergeben, bitte wähle einen anderen!", "danger")
                    return redirect(url_for("register"))

            json_data["page-users"][email] = {"nickname": nickname, "password": hashed_passwod[0], "password_salt": hashed_passwod[1]}
            json_db.write(json_data)
            py_send_mail.send_mail(email, "Registrierung bei Software-Dieburg Games - Quiz", "Vielen Dank für Ihre Registrierung")
            flash("Sie haben Sich erfolgreich ergistriert!", "success")
            return redirect(url_for("login"))
        else:
            flash("Alle Felder müssen ausgefüllt sein!", "danger")

    return render_template("register.html", form=form, json_data=json_data)

# ----------------------------------------------------------------------------------------- #

@app.route("/login/forgot_password", methods=["GET", "POST"])
def forgot_password():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()

	if request.method == "POST":
		email = str(form.login_email.data)
		if email in json_data["page-users"]:
			random_password = app_functions.generateRandomPassword()
			hashed_password = app_functions.password_hash(random_password)
			py_send_mail.send_mail(email, "Neues Passwort bei Software-Dieburg", "Ihr neues Passwort lautet:<br><br>{}<br><br>".format(random_password))
			json_data["page-users"][email]["password"] = hashed_password[0]
			json_data["page-users"][email]["password_salt"] = hashed_password[1]
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
# ----------------------------------------------------------------------------------------- #

@app.route('/', methods=["GET", "POST"])
def home():
    form = HTML_Forms.Form(request.form)
    json_data = json_db.read()
    json_data_ip = json_db.read("ip")
    tmp_data = app_functions.getGeoIPData(request.remote_addr)

    json_data_ip[tmp_data["ip"]] = tmp_data
    if "last-visit" not in json_data_ip[tmp_data["ip"]]:
        json_data_ip[tmp_data["ip"]]["last-visit"] = {"new":str(datetime.datetime.now()) ,"old": "1999-01-01 00:00:00:000000"}
    else:
        json_data_ip[tmp_data["ip"]]["last-visit"]["old"] = json_data_ip[tmp_data["ip"]]["last-visit"]["new"]
        json_data_ip[tmp_data["ip"]]["last-visit"]["new"] = str(datetime.datetime.now())
    json_db.write(json_data_ip, "ip")
    return render_template("home.html", form=form, json_data=json_data)
# ----------------------------------------------------------------------------------------- #

@app.route('/quiz/<string:id>', methods=["GET", "POST"])
def quiz(id):
    json_data = json_db.read()

    if "nickname" not in session:
        flash("Sieht aus als wärst du nicht mehr eingeloggt.", "info")
        return redirect(url_for("login"))

    if "users" not in json_data:
            json_data["users"] = {}
    if session["nickname"] not in json_data["users"]:
        json_data["users"][session["nickname"]] = {}

    if "tmp-group" not in json_data["users"][session["nickname"]]:
        tmp_dict = json_data["groups"][id].copy()
        json_data["users"][session["nickname"]]["tmp-group"] = py_quiz.makeQuiz(tmp_dict)
        json_data["users"][session["nickname"]]["tmp-group"]["group-name"] = id
        json_data["users"][session["nickname"]]["tmp-group"]["question-index"] = 0
        json_data["users"][session["nickname"]]["tmp-group"]["ts-start"] = str(datetime.datetime.now())
        json_db.write(json_data)
        flash("Viel Spaß bei dem Quiz \'{}\'".format(id), "info")
        return redirect(url_for("quiz", id=id))
    
    

    if request.method == "POST":
        post_data = str(request.get_data())[2:-1]
        post_answer = post_data[-1:].lower()

        right_answer = json_data["users"][session["nickname"]]["tmp-group"]["open-questions"][str(json_data["users"][session["nickname"]]["tmp-group"]["question-index"])]["right-answer"]
        user_answer  =json_data["users"][session["nickname"]]["tmp-group"]["open-questions"][str(json_data["users"][session["nickname"]]["tmp-group"]["question-index"])]["answers"][post_answer]
        json_data["users"][session["nickname"]]["tmp-group"]["question-index"] += 1
        
        if user_answer == right_answer:
            flash("Richtig","success")
            if "right-answers" not in json_data["users"][session["nickname"]]["tmp-group"]["used-questions"]:
                json_data["users"][session["nickname"]]["tmp-group"]["used-questions"]["right-answers"] = 0
            json_data["users"][session["nickname"]]["tmp-group"]["used-questions"]["right-answers"] += 1
        else:
            flash("Falsch", "danger")
            if "right-answers" not in json_data["users"][session["nickname"]]["tmp-group"]["used-questions"]:
                json_data["users"][session["nickname"]]["tmp-group"]["used-questions"]["right-answers"] = 0
        
        json_db.write(json_data)
    
    if json_data["users"][session["nickname"]]["tmp-group"]["question-index"] == len( json_data["users"][session["nickname"]]["tmp-group"]["open-questions"]):
        count_right_answers = json_data["users"][session["nickname"]]["tmp-group"]["used-questions"]["right-answers"]
        count_questions = len(json_data["users"][session["nickname"]]["tmp-group"]["open-questions"])
        
        time_difference = app_functions.datetimeTimeDifference(app_functions.string2datetime(json_data["users"][session["nickname"]]["tmp-group"]["ts-start"]), datetime.datetime.now())
        
        if "user-trys" not in json_data["groups"][id]:
            json_data["groups"][id]["user-trys"] = {}
        if session["nickname"] not in json_data["groups"][id]["user-trys"]:
            json_data["groups"][id]["user-trys"][session["nickname"]] = 0
        json_data["groups"][id]["user-trys"][session["nickname"]] += 1
        if "leaderboard" not in json_data["groups"][id]:
            json_data["groups"][id]["leaderboard"] = {}
        json_data["groups"][id]["leaderboard"][len(json_data["groups"][id]["leaderboard"])] = {"nickname": session["nickname"], "right-answers": count_right_answers, "questions": count_questions, "time": time_difference, "trys": json_data["groups"][id]["user-trys"][session["nickname"]]}
        flash("Das Quiz ist vorbei! Ich hoffe du hattest Spaß und warst erfolgreich! Du hast {} Fragen von {} richtig beantwortet! In einer Zeit von {}".format(count_right_answers, count_questions, time_difference), "info")
        del json_data["users"][session["nickname"]]["tmp-group"]
        json_db.write(json_data)
        return redirect(url_for("quiz_lobby"))


    return render_template("quiz.html", json_data=json_data, id=id)
# ----------------------------------------------------------------------------------------- #

@app.route('/quiz_leaderboard/<string:id>', methods=["GET", "POST"])
def quiz_leaderboard(id):
    json_data = json_db.read()

    if "leaderboard" not in json_data["groups"][id]:
        json_data["groups"][id]["leaderboard"] = {}
    

    leaderboad = py_quiz.makeRanking(json_data["groups"][id]["leaderboard"])
    json_data["groups"][id]["leaderboard"] = leaderboad

    json_db.write(json_data)
    return render_template("quiz_leaderboard.html", json_data=json_data, id=id)
# ----------------------------------------------------------------------------------------- #

@app.route('/quiz_lobby', methods=["GET", "POST"])
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

    if "nickname" not in session:
        flash("Sieht aus als wärst du nicht mehr eingeloggt.", "info")
        return redirect(url_for("login"))

    if request.method == "POST":
        title = form.quiz_title.data
        tmp_mode = form.quiz_mode.data
        mode = ""
        if tmp_mode == "Jeder darf Fragen und Antworten erstellen":
            mode = "rw"
        else:
            mode = "r"
        
        if "groups" not in json_data:
            json_data["groups"] = {}
        json_data["groups"][title] = {"mode": mode, "owner": session["nickname"]}
        
        json_db.write(json_data)
        return redirect(url_for("quiz_lobby"))

    json_db.write(json_data)
    return render_template("quiz_create_new_lobby.html", form=form, json_data=json_data)
# ----------------------------------------------------------------------------------------- #

@app.route('/quiz_show/<string:id>', methods=["GET", "POST"])
def quiz_show(id):
    form = HTML_Forms.Form(request.form)
    json_data = json_db.read()

    if "nickname" not in session:
        flash("Sieht aus als wärst du nicht mehr eingeloggt.", "info")
        return redirect(url_for("login"))

    if session["nickname"] != json_data["groups"][id]["owner"]:
        flash("Sie haben keine Berechtigung auf diese Gruppe zuzugreifen!", "danger")
        return redirect(url_for("quiz_lobby"))
    
    if request.method == "POST":
        question = form.question.data
        right_answer = form.answer_a.data
        answer_b = form.answer_b.data
        answer_c = form.answer_c.data
        answer_d = form.answer_d.data

        if question == "" or right_answer == "" or answer_b == "" or answer_c == "" or answer_d == "":
            flash("Bitte fülle alle Felder aus!", "danger")
            return redirect(url_for("quiz_show", id=id))

        if "questions" not in json_data["groups"][id]:
            json_data["groups"][id]["questions"] = {}
        
        if question not in json_data["groups"][id]["questions"]:
            json_data["groups"][id]["questions"][question] = {}
            json_data["groups"][id]["questions"][question]["a"] = right_answer
            json_data["groups"][id]["questions"][question]["b"] = answer_b
            json_data["groups"][id]["questions"][question]["c"] = answer_c
            json_data["groups"][id]["questions"][question]["d"] = answer_d
            json_db.write(json_data)
            flash("Die Frage wurde hinzugefügt", "success")
            return redirect(url_for("quiz_show",id=id))
        else:
            flash("Diese Frage existiert bereits!", "danger")
            return redirect(url_for("quiz_show",id=id))

    return render_template("quiz_show.html", form=form, json_data=json_data, id=id)
# ----------------------------------------------------------------------------------------- #

@app.route('/del_group/<string:id>', methods=["GET", "POST"])
def delete_goup(id):
    json_data = json_db.read()
    if session["nickname"] == json_data["groups"][id]["owner"]:
        del json_data["groups"][id]
        json_db.write(json_data)
        flash("Du hast die Gruppe gelöscht!", "success")
    else:
        flash("Du hast keine Berechtigung das zu tun!", "danger")
    return redirect(url_for("quiz_lobby"))
# ----------------------------------------------------------------------------------------- #

@app.route('/del_question/<string:id>/<string:question>/', methods=["GET", "POST"])
def delete_question(id, question):
    json_data = json_db.read()
    if session["nickname"] == json_data["groups"][id]["owner"]:
        question_list = list(json_data["groups"][id]["questions"])
        del json_data["groups"][id]["questions"][str(question_list[int(question)])]
        json_db.write(json_data)
        flash("Du hast die Frage gelöscht!", "success")

    else:
        flash("Du hast keine Berechtigung das zu tun!", "danger")
    return redirect(url_for("quiz_show", id=id))
# ----------------------------------------------------------------------------------------- #

@app.route('/admin', methods=["GET", "POST"])
def admin():
    json_data = json_db.read()
    json_data_ip = json_db.read("ip")
    
    if "admin" not in json_data["users"][session["nickname"]]:
        return redirect(url_for("quiz_lobby"))

    return render_template("admin.html", json_data=json_data, json_data_ip=json_data_ip)
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
