# -*- coding:utf-8 -*-
# Compiled with Python 3.7

import time
import os
import urllib3
import base64
import requests
from http import cookiejar

class seuhelper:

	usr = ""
	pwd = ""
	session = ""
	str_check = ["\\u7528\\u6237\\u5df2\\u767b\\u5f55", "\\u8ba4\\u8bc1\\u6210\\u529f", "ALREADY_LOGIN", "INVALID_LOCATION", "\\u5730\\u5740\\u9519\\u8bef"]
	url_login = "http://w.seu.edu.cn/index.php/index/login"
	url_logout = "http://w.seu.edu.cn/index.php/index/logout"
	url_login_sub = "https://w.seu.edu.cn/index.php/index/login"
	url_logout_sub = "https://w.seu.edu.cn/index.php/index/logout"
	url_host = "http://w.seu.edu.cn/"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
	           'Origin': 'http://w.seu.edu.cn', 'Referer': 'http://w.seu.edu.cn/',
	           'Host': 'w.seu.edu.cn', 'X-Requested-With': 'XMLHttpRequest'}

	def __init__(self, usr, pwd):
		self.usr = usr
		self.pwd = base64.b64encode(pwd.encode('utf-8')).decode('utf-8')    # 学校登录页面对密码进行了BASE64加密
		# 思路来源：http://w.seu.edu.cn/Modules/Home/Public/Js/login.js
		self.session = requests.Session()
		self.session.cookies = cookiejar.CookieJar()
		self.check_ssl()    # 1228 Update : SSL check

	def check_ssl(self):
		try:
			self.session.get(self.url_host, headers=self.headers)
		except:
			self.url_login = self.url_login_sub
			self.url_logout = self.url_logout_sub
			print("检测到校园网安全协议变更，已自动为您更换接口...")

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
			print("登录失败，请检查密码是否正确！\n如密码正确，请检查网络账户是否正常续费！")

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
		# 1204 去除冗余提醒
		print("您的计算机将会每隔" + str(interval) + "分钟检测一次校园网登录状态\n若想退出自动检测，请直接退出程序。")
		secsPortion = interval * 60 / 5    # 输入分钟，转换成秒，按照5秒切分，以免进程被锁
		last_status = False
		while True:
			if self.check_status():
				if not last_status:
					print("用户:" + str(self.usr) + " 已在登录状态，等待下次检测...")
					last_status = True
				else:
					print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + " 检测通过√")
			else:
				print("用户未登录，准备自动登录中...")
				self.command_login()
				last_status = False
			for i in range(int(secsPortion)):
				time.sleep(5.0)

	# 读取html
	def login(self, htmlUrl='', data={}, method='POST'):
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		time.sleep(0.2)  # 防止封IP
		if htmlUrl == '':
			htmlUrl = self.url_login
		try:
			if method.upper() == 'GET':
				r = self.session.get(htmlUrl, headers=self.headers, data=data, verify=False)
			else:
				r = self.session.post(htmlUrl, headers=self.headers, data=data, verify=False)
		except:
			print("计算机网络连接出现问题，准备执行自动修复，请稍等...")
			os.system("ipconfig /release")
			os.system("ipconfig /renew")
			os.system("cls")
			print("修复完成，准备尝试重新操作...")
			try:
				if method.upper() == 'GET':
					r = self.session.get(htmlUrl, headers=self.headers, data=data)
				else:
					r = self.session.post(htmlUrl, headers=self.headers, data=data)
			except:
				print("网络连接出现严重问题无法修复，请自行检查计算机配置")
				return ""
		return r.text