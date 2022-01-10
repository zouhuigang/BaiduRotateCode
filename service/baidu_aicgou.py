# -*- coding: UTF-8 -*-

from time import sleep

from service.analyze import Analyze
from service.ui_operate import UiOperate


class BaiduAicgou():
	PASSPORT_URL = "https://b2b.baidu.com/s?q=%E6%B0%B4%E6%B3%A5&from=search&fid=0%2C1641256982298&pi=b2b.s.search...826060690047366";

	def __init__(self, account):
		self.account = account
		self.ui = UiOperate(account["serverIp"])
		pass

	def b2b(self):
		# 打开页面
		self.ui.get(self.PASSPORT_URL)
		sleep(2)
		# 点击更多按钮
		flag = self.ui.isElementExist(self.ui.xpath("//*[starts-with(@class,'sj-filter-category')]"))
		if flag:
			items = self.ui.getEles(self.ui.xpath("//*[starts-with(@class,'sj-filter-category')]"))
			print(items)
			for item in items:
				html = item.get_attribute("innerHTML")
				print(html)

	# flag = self.ui.isElementExist(self.ui.xpath("//em[@class='unfold']"))
	# while flag:
	# 	self.ui.click(self.ui.xpath("//em[@class='unfold']"))
	# 	flag = self.ui.isElementExist(self.ui.xpath("//em[@class='unfold']"))
	# 	sleep(1)
