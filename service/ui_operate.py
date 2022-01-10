# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import random
import json
import time


# ui操作类
class UiOperate():

	def __init__(self, xff):
		self.driver = self.initDriver(xff)
		pass

	# 控制浏览器
	def initDriver(self, xff):
		# 加启动配置
		option = webdriver.ChromeOptions()
		# 关闭“chrome正受到自动测试软件的控制”
		# V75以及以下版本
		# option.add_argument('disable-infobars')
		# V76以及以上版本
		option.add_experimental_option('useAutomationExtension', False)
		option.add_experimental_option('excludeSwitches', ['enable-automation'])
		# 不自动关闭浏览器
		option.add_experimental_option("detach", True)
		# 更换头部
		# option.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"')
		# 39.99.159.171
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
		option.add_argument('--user-agent=%s' % user_agent)
		# xff = "39.99.159.171"
		option.add_argument('--X-Forwarded-for=%s' % xff)
		driver = webdriver.Chrome(chrome_options=option)
		return driver

	def get(self, url):
		return self.driver.get(url)

	# 拖动
	def drag_and_drop(self, element, offset):
		action = ActionChains(self.driver)
		ele = self.driver.find_element(*element)
		action.drag_and_drop_by_offset(ele, offset, 0).perform()

	# 点击
	def click(self, element):
		flag = self.isElementExist(element)
		action = ActionChains(self.driver)
		count = 0
		if not flag:
			while not flag and count < 3:
				time.sleep(1)
				flag = self.isElementExist(element)
				count = count + 1
				print("warning: try again ", element[1])
		else:
			# driver.find_element(*element).click()
			ele = self.driver.find_element(*element)
			action.move_to_element(ele).click().perform()
			return True

		if not flag:
			print("warning: not found ", element[1])
			return False
		else:
			# driver.find_element(*element).click()
			ele = self.driver.find_element(*element)
			action.move_to_element(ele).click().perform()
			return True

	# 输入
	def send_keys(self, element, str):
		flag = self.isElementExist(element)
		count = 0
		if not flag:
			while not flag and count < 3:
				time.sleep(1)
				flag = self.isElementExist(element)
				count = count + 1
				print("warning:try again ", element[1])
		else:
			self.driver.find_element(*element).send_keys(str)
			return True

		if not flag:
			print("warning: not found ", element[1])
			return False
		else:
			self.driver.find_element(*element).send_keys(str)
			return True

	# 判断元素是否存在
	def isElementExist(self, element):
		try:
			WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(element))
			return True
		except selenium.common.exceptions.TimeoutException:
			return False
		except selenium.common.exceptions.NoSuchElementException:
			return False

	# 获取src或href中的属性,name = src或href
	def getAttribute(self, ele, name="href"):
		# ele = driver.find_element(*(By.XPATH, "//*[starts-with(@id,'vcode-spin-img')]"))
		ele = self.driver.find_element(*(ele))
		return ele.get_attribute(name)

	def getEles(self, ele):
		return self.driver.find_elements(*(ele))

	# 存储cookie
	def download_cookie(self, cookie_file):

		cookies = self.driver.get_cookies()

		with open(cookie_file, 'w') as fp:
			fp.write(json.dumps(cookies))
			"""将获取到的登录态user_session，写入文件，供后续调用"""
			print(u"cookie已写入文件" + cookie_file)

	# 加载cookie到driver
	def load_cookie(self, cookie_file):
		# 读取cookie & 加载
		with open(cookie_file, 'r+') as fp:
			cookies = fp.read()
			cookies_list = json.loads(cookies)
		for dic in cookies_list:
			if 'expiry' in dic:
				del dic['expiry']
			# sleep(0.01)
			self.driver.add_cookie(dic)

	# 添加cookie
	def addCookie(self, cookie_str):
		cookies_list = json.loads(cookie_str)
		for dic in cookies_list:
			if 'expiry' in dic:
				del dic['expiry']
			# sleep(0.01)
			self.driver.add_cookie(dic)

	# 根据xpath定位元素
	# Chrome调试：Console调试$x("//*[starts-with(@id,'vcode-spin-button')]")
	# VCODE_BTN = (By.XPATH, "//*[starts-with(@id,'vcode-spin-button')]")
	def xpath(self, xpa):
		return (By.XPATH, xpa)

	# 根据class定位
	def byClass(self, sel):
		return (By.CLASS_NAME, sel)

	# 控制隐藏元素
	def control_in_shadow(self, js):
		shadow = self.driver.execute_script(js)
		return shadow  # 返回的对象在这里

	def expand_shadow_element(self, element):
		shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
		return shadow_root

	# 获取元素的width和height
	def getSize(self, ele):
		ele = self.driver.find_element(*(ele))
		return ele.size

	def get_track(self, distance):
		"""
		模拟轨迹 假装是人在操作
		:param distance:
		:return:
		"""
		# 初速度
		v = 0
		# 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
		t = 0.2
		# 位移/轨迹列表，列表内的一个元素代表0.2s的位移
		tracks = []
		# 当前的位移
		current = 0
		# 到达mid值开始减速
		mid = distance * 7 / 8

		distance += 10  # 先滑过一点，最后再反着滑动回来
		# a = random.randint(1,3)
		while current < distance:
			if current < mid:
				# 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
				a = random.randint(2, 4)  # 加速运动
			else:
				a = -random.randint(3, 5)  # 减速运动

			# 初速度
			v0 = v
			# 0.2秒时间内的位移
			s = v0 * t + 0.5 * a * (t ** 2)
			# 当前的位置
			current += s
			# 添加到轨迹列表
			tracks.append(round(s))

			# 速度已经达到v,该速度作为下次的初速度
			v = v0 + a * t

		# 反着滑动到大概准确位置
		for i in range(4):
			tracks.append(-random.randint(2, 3))
		for i in range(4):
			tracks.append(-random.randint(1, 3))
		return

	def after_quit(self):
		"""
		关闭浏览器
		"""
		self.driver.quit()
