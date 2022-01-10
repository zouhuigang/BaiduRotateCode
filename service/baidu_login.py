# -*- coding: UTF-8 -*-

import os
import json
import time
from telnetlib import EC
from time import sleep

import selenium
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LoginEvent():

	def __init__(self):
		pass

	def read_file(path):
		with open(path, 'r', encoding="utf-8") as f:
			content = f.read()
		return content

	# 替换Selenium Session ID
	seqNo = 2

	user_name = ""
	password = ""
	user_id = ""

	json_file_str = read_file('baidu_account.json')
	account_data = json.loads(json_file_str)
	for account in account_data:
		if account['seqNo'] == seqNo:
			user_name = account['userName']
			password = account['passwd']
			user_id = account['userId']
			break


	LOGIN_RUKOU = (By.CLASS_NAME, 'tab-log-type')
	LOGIN_SWITCH = (By.XPATH, ".//*[@id='user-tools']/li[2]/a[1]")
	USER_NAME = (By.XPATH, ".//*[@id='uc-common-account']")
	PASSWORD = (By.XPATH, ".//*[@id='ucsl-password-edit']")
	LOGIN_BTN = (By.XPATH, ".//*[@id='submit-form']")


	# login_url = "https://cas.baidu.com/?tpl=www2&fromu=https%3A%2F%2Ffengchao.baidu.com%2Fhairuo%2Fmain.do%3Fuserid%3D" + user_id + "%26rurl%3DaHR0cHM6Ly9mZW5nY2hhby5iYWlkdS5jb20vZmMvbWFuYWdlL3Rvb2xzL3VzZXIvMzA1MTMwMTMvYWRwcmV2aWV3P2Zyb209bmF2"
	# page_url = "https://fengchao.baidu.com/fc/manage/tools/user/" + user_id+ "/adpreview?from=nav"
	login_url = "https://cas.baidu.com/?tpl=www2&fromu=https%3A%2F%2Ffengchao.baidu.com%2Fhairuo%2Fmain.do%3Fuserid%3D" + user_id \
	            + "%26rurl%3DaHR0cHM6Ly9mZW5nY2hhby5iYWlkdS5jb20vZmMvdG9vbHNjZW50ZXIvb3B0aW1pemUvYWRwcmV2aWV3QW5kRGlhZ25vc2UvdXNlci8zMDUxMjk0Ny90eXBlL2FkcHJldmlldw%3D%3D"
	page_url = "https://fengchao.baidu.com/fc/toolscenter/optimize/adpreviewAndDiagnose/user/" + user_id+ "/type/adpreview"

	def login_cookie_check_read(self, driver):
		# 获取配置信息
		app="baidu"

		cookie_file = 'sem_cookie_01.txt'

		# driver.get('https://fengchao.baidu.com/404.html')
		driver.get(self.login_url)

		# 判断cookie文件是否存在，不存在则需要重新登录
		# if (not os.path.isfile(cookie_file)):
		#     print("cookie文件不存在，触发登录：" + cookie_file)
		#     # 触发登录

		self.login(driver, app, self.login_url, self.user_name, self.password, cookie_file)

		# 加载cookie
		# self.load_cookie(driver,self.login_url, cookie_file)

		driver.get(self.page_url)
		time.sleep(5)

		inputElement = driver.find_element_by_css_selector("input.one-search-box")
		inputElement.send_keys("搬家")

		# self.click_button_byText(driver, '查询排名实况')
		buttonElement = driver.find_element_by_css_selector("button.one-button-primary")
		buttonElement.click()

		time.sleep(5)
		# self.download_cookie(driver, cookie_file)

		iframe = driver.find_elements_by_tag_name("iframe")[0]
		driver.switch_to_frame(iframe)

		print(driver.page_source)

	def click_button_byText(self, driver, text):
		try:
			elements = driver.find_elements('tag name', 'button')
			for i in elements:
				print(i.get_attribute("textContent"))
				if i.get_attribute("textContent").find(text) >= 0:
					i.click()
					break
		except AttributeError:
			print(u"页面中未能找到 %s 元素" % (text))


	"""
		触发登录接口： 根据登录url进入到登录页面， 填入用户名密码， 提交登录。 将登录后的cookie存储到固定文件。
		注： 此处暂时不考虑  一个账号需要同时触发login的场景。 后续如有需要可以在这里防一下。
	"""
	def login(self, driver, app, login_url ,user_name, password, cookie_file ):
		# 先自己退出下
		driver.delete_all_cookies()
		# 进行登录
		sleep(1)
		if app == "baidu":
			# self.click(driver, self.LOGIN_RUKOU)
			# sleep(1)
			self.send_keys(driver, self.USER_NAME, user_name)
			sleep(1)
			self.send_keys(driver, self.PASSWORD, password)
			sleep(10)
			self.click(driver, self.LOGIN_BTN)
			sleep(2)

		else:
			print(u"不支持的业务线登录，需要去login.py中进行配置,退出python")
			driver.quit()
			os._exit(1)
		# todo 其他登录方在这里补充


		print(u'login success')

		# 存储cookie TODO
		self.download_cookie(driver, cookie_file)




	"""       
		 存储cookie
	"""

	def download_cookie(self, driver ,cookie_file):

		cookies = driver.get_cookies()

		# driver.get("https://cas.baidu.com")
		# cookies1 = driver.get_cookies()

		# for casCookie in cookies1:
		#     if casCookie['name'] == 'CASSSID':
		#         cookies.append(casCookie)
		#         break

		with open(cookie_file, 'w') as fp:
			fp.write(json.dumps(cookies))
			"""将获取到的登录态user_session，写入文件，供后续调用"""
			print(u"cookie已写入文件" + cookie_file)



	"""       
		加载cookie到driver
	"""
	def load_cookie(self, driver ,login_url,cookie_file):
		# 读取cookie & 加载
		with open(cookie_file, 'r+') as fp:
			cookies = fp.read()
			cookies_list = json.loads(cookies)
		for dic in cookies_list:
			if 'expiry' in dic:
				del dic['expiry']

			#sleep(0.01)
			driver.add_cookie(dic)


		driver.get(self.page_url)

	def click(self, driver, element):
		flag = self.isElementExist(driver, element)
		count = 0
		if not flag:
			while not flag and count < 3:
				time.sleep(1)
				flag = self.isElementExist(driver, element)
				count = count + 1
				print("warning: try again ",element[1])
		else:
			driver.find_element(*element).click()
			return True

		if not flag:
			print("warning: not found ", element[1])
			return False
		else:
			driver.find_element(*element).click()
			return True

	def send_keys(self, driver, element, str):
		flag = self.isElementExist(driver, element)
		count = 0
		if not flag:
			while not flag and count < 3:
				time.sleep(1)
				flag = self.isElementExist(driver, element)
				count = count + 1
				print("warning:try again ", element[1])
		else:
			driver.find_element(*element).send_keys(str)
			return True

		if not flag:
			print("warning: not found ", element[1])
			return False
		else:
			driver.find_element(*element).send_keys(str)
			return True

	def isElementExist(self, driver, element):
		try:
			WebDriverWait(driver, 5).until(EC.visibility_of_element_located(element))
			return True
		except selenium.common.exceptions.TimeoutException:
			return False
		except selenium.common.exceptions.NoSuchElementException:
			return False
