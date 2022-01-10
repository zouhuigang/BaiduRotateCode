# -*- coding: UTF-8 -*-

import random

from service.baidu_aicgou import BaiduAicgou


def random_ipv4():
	ip = '%i.%i.%i.%i' % (
		random.randint(10, 235),
		random.randint(10, 235),
		random.randint(10, 235),
		random.randint(10, 235)
	)
	return ip


def call_baidu_train_data():
	account = {}
	account["serverIp"] = random_ipv4()
	print(account)
	loginEvent = BaiduAicgou(account)
	loginEvent.b2b()


if __name__ == "__main__":
	call_baidu_train_data()
