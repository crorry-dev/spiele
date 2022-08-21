#-*- coding:utf-8 -*-
import random, datetime

def makeQuiz(group_data):
    open_questions = {}
    used_questions = {}
    index = 0

    tmp_questions = group_data["questions"].copy()
    while len(tmp_questions) > 0:
        r = random.randint(0, len(tmp_questions)-1)
        for i, question in enumerate(tmp_questions):
            print(i, question)
            if r == i:
                open_questions[index] = {"question": question}
                open_questions[index]["right-answer"] =  tmp_questions[question]["a"]
                open_questions[index]["answers"] = {}

                tmp_answers = [tmp_questions[question]["a"], tmp_questions[question]["b"], tmp_questions[question]["c"], tmp_questions[question]["d"]]
                while len(tmp_answers) > 0:
                    r_a = random.randint(0, len(tmp_answers)-1)
                    if "a" not in open_questions[index]["answers"]:
                        open_questions[index]["answers"]["a"] = tmp_answers[r_a]
                        del tmp_answers[r_a]
                    elif "b" not in open_questions[index]["answers"]:
                        open_questions[index]["answers"]["b"] = tmp_answers[r_a]
                        del tmp_answers[r_a]
                    elif "c" not in open_questions[index]["answers"]:
                        open_questions[index]["answers"]["c"] = tmp_answers[r_a]
                        del tmp_answers[r_a]
                    elif "d" not in open_questions[index]["answers"]:
                        open_questions[index]["answers"]["d"] = tmp_answers[r_a]
                        del tmp_answers[r_a]
                index += 1
                del tmp_questions[question]
                break
                
    return {"open-questions": open_questions, "used-questions": used_questions}


def makeRanking(leaderboard_data):
    # pos: {nickname: "", right-answers: 1, questions: 2, time: 0:0:6.213, trys: 1}
    tmp_leaderboad = leaderboard_data.copy()
    leaderboad = []
    for r in tmp_leaderboad:
        leaderboad.append(tmp_leaderboad[r])
    
    for r in range(len(leaderboad)):
        for rr in range(0, len(leaderboad) - r - 1):
            if leaderboad[rr]["right-answers"] > leaderboad[rr + 1]["right-answers"]:
                tmp = leaderboad[rr]
                leaderboad[rr] = leaderboad[rr+1]
                leaderboad[rr+1] = tmp
            elif leaderboad[rr]["right-answers"] == leaderboad[rr + 1]["right-answers"]:
                if leaderboad[rr]["trys"] < leaderboad[rr + 1]["trys"]:
                    tmp = leaderboad[rr]
                    leaderboad[rr] = leaderboad[rr+1]
                    leaderboad[rr+1] = tmp
                elif leaderboad[rr]["trys"] == leaderboad[rr + 1]["trys"]:
                    if datetime.datetime.strptime(leaderboad[rr]["time"], "%H:%M:%S.%f") < datetime.datetime.strptime(leaderboad[rr + 1]["time"], "%H:%M:%S.%f"):
                        tmp = leaderboad[rr]
                        leaderboad[rr] = leaderboad[rr+1]
                        leaderboad[rr+1] = tmp
    
    return_leaderboard = {}
    index = 0
    for r in range(len(leaderboad)-1,-1, -1):
        return_leaderboard[str(index)] = leaderboad[r]
        index += 1
    
    return return_leaderboard


