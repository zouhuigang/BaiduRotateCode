# -*- coding: UTF-8 -*-

import urllib.request
import os
import datetime


# image操作类
class Image():

	def __init__(self, dest):
		os.makedirs(dest, exist_ok=True)
		self.dest = dest
		pass

	def percentage(self, a, b, c):
		'''''
		a:已经下载的数据块
		b:数据块的大小
		c:远程文件的大小
		'''
		per = 100.0 * a * b / c
		if per > 100:
			per = 100
		print('%.2f%%' % per)

	def download(self, imgurl, ext):
		"""
		https://github.com/ybsdegit/captcha_qq/blob/master/captcha_qq.py
		下载图片
		:param imgurl: 图片url
		:param imgsavepath: 存放地址 './image/slideBlock.png'
		"""
		imgsavepath = self.dest + "/" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ext
		# 添加header
		opener = urllib.request.build_opener()
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
		opener.addheaders = [('User-agent', user_agent)]
		urllib.request.install_opener(opener)

		urllib.request.urlretrieve(imgurl, imgsavepath, self.percentage)
		print(imgsavepath)
