# -*- coding:utf-8 -*-
# Compiled with Python 3.7

import time
import base64
import requests
from http import cookiejar

class seuhelper:

	usr = ""
	pwd = ""
	session = ""
	str_check = ["\\u7528\\u6237\\u5df2\\u767b\\u5f55", "\\u8ba4\\u8bc1\\u6210\\u529f", "ALREADY_LOGIN"]
	url_login = "http://w.seu.edu.cn/index.php/index/login"
	url_logout = "http://w.seu.edu.cn/index.php/index/logout"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
	           'Origin': 'http://w.seu.edu.cn', 'Referer': 'http://w.seu.edu.cn/',
	           'Host': 'w.seu.edu.cn', 'X-Requested-With': 'XMLHttpRequest'}

	def __init__(self, usr, pwd):
		self.usr = usr
		self.pwd = base64.b64encode(pwd.encode('utf-8')).decode('utf-8')    # 学校登录页面对密码进行了BASE64加密
		# 思路来源：http://w.seu.edu.cn/Modules/Home/Public/Js/login.js
		self.session = requests.Session()
		self.session.cookies = cookiejar.CookieJar()

	def check_str(self, dict, text):
		for item in dict:
			if str(text).__contains__(item):
				return True
		return False

	def command_login(self):
		params = {'username': self.usr, 'password': self.pwd, 'enablemacauth': 0}
		resptext = self.login(self.url_login, data=params)
		if self.check_str(self.str_check, resptext):
			print("用户:" + self.usr + " 登录成功！")
		else:
			print("登录失败，请检查密码是否正确！")

	def command_logout(self):
		resptext = self.login(self.url_logout)
		if self.check_str(self.str_check, resptext):
			print("注销登录失败，请检查网路连接！")
		else:
			print("用户:" + self.usr + " 已注销登录！")

	def check_status(self):
		resptext = self.login(self.url_login)
		if self.check_str(self.str_check, resptext):
			return True # 已经登录
		else:
			return False  # 用户未登录

	def keep_alive(self, interval=10):
		print("您的计算机将会每隔" + str(interval) + "分钟检测一次校园网登录状态\n若想退出自动检测，请直接退出程序。")
		interval = interval * 60    # 输入分钟，转换成秒
		while True:
			if self.check_status():
				print("用户已在登录状态，等待下次检测...")
			else:
				print("用户未登录，准备自动登录中...")
				self.command_login()
			time.sleep(interval)

	# 读取html
	def login(self, htmlUrl='', referer='http://w.seu.edu.cn/', data={}, method='POST'):
		time.sleep(0.2)  # 防止封IP
		if htmlUrl == '':
			htmlUrl = self.url_login
		try:
			if method.upper() == 'GET':
				r = self.session.get(htmlUrl, headers=self.headers, data=data)
			else:
				r = self.session.post(htmlUrl, headers=self.headers, data=data)
		except:
			raise Exception("网络链接出现问题")
		return r.text