# -*- coding: UTF-8 -*-

from time import sleep

from service.analyze import Analyze
from service.ui_operate import UiOperate
from service.image import Image
import json
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class LoginEvent():
	PASSPORT_URL = "https://passport.baidu.com/?getpassindex&tt=1640312846951&gid=4914C83-BF2D-40F5-9EB0-197F5C9A50BD&tpl=pp&u=https%3A%2F%2Fpassport.baidu.com%2F";

	QUERY_URL = "https://fengchao.baidu.com/fc/toolscenter/optimize/adpreviewAndDiagnose/user/%s/type/adpreview"

	def __init__(self, account):
		self.account = account
		self.ui = UiOperate(account["serverIp"])
		self.image = Image("./images")
		pass

	def checkQuery(self):
		self.ui.get("https://fengchao.baidu.com/404.html")
		self.ui.addCookie(self.account["cookie"])
		sleep(1)
		self.ui.get((self.QUERY_URL % self.account["userId"]))
		sleep(5)
		# <a href="link_with_key_word_in.html">Link</a> => By.xpath("//a[contains(@href, 'key_word')]"));
		# 被#shadow-root (open)标记的元素不能被定位到 https://blog.csdn.net/dyfDewey/article/details/116454716
		# https://www.codeleading.com/article/7411963224/
		# https://github.com/justicemswann/CRF_Rasberry_Pi_Scripts/blob/80330caef252c2f897a6502a864c752bbeef40c8/crf_ha_scraper.py
		js = "return document.querySelector('#hm-circular').shadowRoot.querySelector(\"div[class*='index__dialogContainer']\").querySelector(\"span[class*='index__button']\")"
		self.ui.control_in_shadow(js).click()

		# 等待输入
		sleep(8)
		# 输入key
		self.ui.send_keys(self.ui.byClass("one-search-box"), "上海搬家")
		# 输入回车
		self.ui.send_keys(self.ui.byClass("one-search-box"), Keys.ENTER)
		sleep(5)
		flag = self.ui.isElementExist(self.ui.xpath("//*[starts-with(@id,'vcode-spin-button')]"))
		print(flag)
		count = 0
		if flag:
			# 加载验证模型
			aiAnalyze = Analyze()
			model_location = aiAnalyze.loadModel()
			while flag and count < 50:
				count = count + 1
				imgUrl = self.ui.getAttribute(self.ui.xpath("//*[starts-with(@id,'vcode-spin-img')]"), "src")
				print("正在进行第%d轮破解\n获取到的旋转验证码为:%s" % (count, imgUrl))
				# 下载验证码，为了数据分析
				self.image.download(imgUrl, ".jpeg")
				angle = aiAnalyze.rotateVerificationCode(model_location, imgUrl)[0]
				# 获取滑动槽的宽度和滑块的宽度
				maxSize = self.ui.getSize(self.ui.xpath("//*[starts-with(@id,'vcode-spin-bottom')]"))
				blockSize = self.ui.getSize(self.ui.xpath("//*[starts-with(@id,'vcode-spin-button')]"))
				print(maxSize, blockSize)
				b = maxSize.get("width") - blockSize.get("width")
				move_line = angle / 360 * b
				print("AI识别到的角度:%s,计算应该滑动的距离为:%s,旋转验证码可移动宽度: %s" % (angle, move_line, b))
				self.ui.drag_and_drop(self.ui.xpath("//*[starts-with(@id,'vcode-spin-button')]"), move_line)
				sleep(5)


	def loginByVerifyCode(self):
		# 打开页面
		self.ui.get(self.PASSPORT_URL)
		sleep(2)
		# 输入用户名和密码
		self.ui.send_keys(self.ui.xpath(".//*[@id='account']"), "asduuq")
		sleep(10)
		self.ui.click(self.ui.xpath("//*[@id='submit']"))
		# 再点一次
		sleep(5)
		self.ui.click(self.ui.xpath("//*[@id='submit']"))
		# 滑动验证码
		sleep(5)
		# knob = driver.find_element_by_class_name("gt_slider_knob")
		flag = self.ui.isElementExist(self.ui.xpath("//*[starts-with(@id,'vcode-spin-button')]"))
		print(flag)
		count = 0
		if flag:
			# 加载验证模型
			aiAnalyze = Analyze()
			model_location = aiAnalyze.loadModel()
			while flag and count < 50:
				count = count + 1
				imgUrl = self.ui.getAttribute(self.ui.xpath("//*[starts-with(@id,'vcode-spin-img')]"), "src")
				print("正在进行第%d轮破解\n获取到的旋转验证码为:%s" % (count, imgUrl))
				# 下载验证码，为了数据分析
				print("正在下载验证码图片")
				self.image.download(imgUrl, ".jpeg")
				angle = aiAnalyze.rotateVerificationCode(model_location, imgUrl)[0]
				# 获取滑动槽的宽度和滑块的宽度
				maxSize = self.ui.getSize(self.ui.xpath("//*[starts-with(@id,'vcode-spin-bottom')]"))
				blockSize = self.ui.getSize(self.ui.xpath("//*[starts-with(@id,'vcode-spin-button')]"))
				print(maxSize, blockSize)
				b = maxSize.get("width") - blockSize.get("width")
				move_line = angle / 360 * b
				print("AI识别到的角度:%s,计算应该滑动的距离为:%s,旋转验证码可移动宽度: %s" % (angle, move_line, b))
				self.ui.drag_and_drop(self.ui.xpath("//*[starts-with(@id,'vcode-spin-button')]"), move_line)
				sleep(10)
