#-*- coding:utf-8 -*-
import random

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