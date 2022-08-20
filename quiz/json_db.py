#-*- coding: utf-8 -*-
import json

DEFAULT_DB_DATA = {}
DBs = []
#pwd = "/home/pi/saufen2go/flask/"
pwd = "./db/"
def write(data={}, filename="db"):
    with open(pwd+filename + ".json", 'w') as file:
        json.dump(data, file, indent=4)
    return data
	
def read(filename="db"):
    with open(pwd+filename + ".json", 'r') as file:
        data = json.load(file)
    return data


def initDB(filename="db"):
    if DBs != []:
        for db in DBs:
            try:
                read(db)
            except FileNotFoundError:
                write(DEFAULT_DB_DATA, db)
    else:
        try:
            read(filename)
        except FileNotFoundError:
            write(DEFAULT_DB_DATA, filename)

initDB()
