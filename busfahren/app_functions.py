#-*- coding:utf-8 -*-
from flask import Flask, request
from uuid import getnode as get_mac
import random, string, hashlib, os, datetime, operator


def getClientInfo():
	ip = request.remote_addr
	browser = request.user_agent.browser
	version = request.user_agent.version and int(request.user_agent.version.split('.')[0])
	platform = request.user_agent.platform
	uas = request.user_agent.string
	mac = get_mac()
	answer = {'ip':ip, 'browser':browser, 'version':version, 'platform':platform, 'uas':uas, 'mac':mac}
	return answer

def password_hash(passwd, salt=None):
	if not salt:
		salt = str(os.urandom(21))[2:-1]
	return str(hashlib.pbkdf2_hmac('sha256', passwd.encode("utf-8"), bytes(salt, "utf-8"), 100000))[2:-1], str(salt)

def generateRandomPassword(length=8):
	result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
	return result_str


def string2datetime(d, t):
	return datetime.datetime.strptime(str(d) + str(t), "%Y-%m-%d %H:%M:%S")



def bubbleSort(array):
  for i in range(len(array)):
    for j in range(0, len(array) - i - 1):
      if array[j] > array[j + 1]:
        temp = array[j]
        array[j] = array[j+1]
        array[j+1] = temp


def sortListInList(_list, sort_by_value=0):
	return sorted(_list, key=operator.itemgetter(sort_by_value))
