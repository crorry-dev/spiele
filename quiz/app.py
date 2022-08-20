#-*- coding:utf-8 -*-
try:
	from flask import Flask, render_template, flash, redirect, url_for, request, session, logging , send_from_directory, send_file
	import random, datetime, re
	import json_db, HTML_Forms, app_functions
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

@app.route('/', methods=["GET", "POST"])
def home():
	form = HTML_Forms.Form(request.form)
	json_data = json_db.read()

	return render_template("home.html", form=form, json_data=json_data)
# ----------------------------------------------------------------------------------------- #

@app.route('/quiz/<string:id>', methods=["GET", "POST"])
def quiz(id):
    json_data = json_db.read()

    if "tmp-group" not in json_data["users"][session["nickname"]]:
        tmp_dict = json_data["groups"][id].copy()
        json_data["users"][session["nickname"]]["tmp-group"] = py_quiz.makeQuiz(tmp_dict)
        json_data["users"][session["nickname"]]["tmp-group"]["question-index"] = 0
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
        flash("Das Quiz ist vorbei! Ich hoffe du hattest Spaß und warst erfolgreich! Du hast {} Fragen von {} richtig beantwortet!".format(count_right_answers, count_questions), "info")
        del json_data["users"][session["nickname"]]["tmp-group"]
        json_db.write(json_data)
        return redirect(url_for("quiz_lobby"))


    return render_template("quiz.html", json_data=json_data, id=id)
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

    if session["nickname"] != json_data["groups"][id]["owner"]:
        flash("Sie haben keine Berechtigung auf diese Gruppe zuzugreifen!", "danger")
        return redirect(url_for("quiz_lobby"))
    
    if request.method == "POST":
        question = form.question.data
        right_answer = form.answer_a.data
        answer_b = form.answer_b.data
        answer_c = form.answer_c.data
        answer_d = form.answer_d.data

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
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #

# App run
if __name__ == "__main__":
	#ipAddress = socket.gethostbyname(socket.gethostname())
	ipAddress = "0.0.0.0"
	app.run(host=ipAddress, port=5002, debug=True)
