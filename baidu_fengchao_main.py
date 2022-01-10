# -*- coding: UTF-8 -*-

from service.baidu_fengchao import LoginEvent
import json
import random

from selenium import webdriver



def read_file(path):
	with open(path, 'r', encoding="utf-8") as f:
		content = f.read()
	return content


def random_ipv4():
	ip = '%i.%i.%i.%i' % (
		random.randint(10, 235),
		random.randint(10, 235),
		random.randint(10, 235),
		random.randint(10, 235)
	)
	return ip


# 滑动验证码
def call_baidu():
	# loginEvent.login_cookie_check_read(driver)
	# loginEvent.loginByVerifyCode()
	seqNo = 26
	json_file_str = read_file('./service/baidu_cookie.json')
	account_data = json.loads(json_file_str)
	for account in account_data:
		if account['seqNo'] == seqNo:
			loginEvent = LoginEvent(account)
			loginEvent.checkQuery()
			break


def call_baidu_train_data():
	account = {}
	account["serverIp"] = random_ipv4()
	print(account)
	loginEvent = LoginEvent(account)
	loginEvent.loginByVerifyCode()




def call_baidu_login_data():
	driver = webdriver.Chrome()
	loginEvent = LoginEvent()
	loginEvent.login_cookie_check_read(driver)


if __name__ == "__main__":
	call_baidu_train_data()
