# -*- coding:utf-8 -*-
# Compiled with Python 3.7

import time
import re
import urllib3
import socket
import requests
import random
from psutil import net_if_addrs
from http import cookiejar

class seuhelper:

	usr = ""
	pwd = ""
	session = ""
	str_check = ["\"ret_code\":0", "ALREADY_LOGIN", "已经登录", "登录成功", "成功登录", "\\u6210\\u529f", "注销成功"]
	str_status = ["\"result\":1"]
	str_filter = ["登录成功标志", "登录失败标志"]
	url_login = "http://202.119.25.2:801/eportal/"
	url_checkstatus = "http://202.119.25.2/drcom/chkstatus"
	url_jsversion = "http://202.119.25.2/a41.js"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
	           'DNT': '1', 'Referer': 'http://202.119.25.2/'}

	def __init__(self, usr, pwd):
		self.usr = usr
		self.pwd = pwd    # 学校登录页面取消了BASE64加密，明文传输，后续更新可能会修复
		# 思路来源：http://w.seu.edu.cn/Modules/Home/Public/Js/login.js
		self.session = requests.Session()
		self.session.cookies = cookiejar.CookieJar()
		self.jsversion = self.get_jsversion()
		self.ipaddr = self.get_my_ip()
		self.macaddr = self.get_mac_address()

	def check_str(self, tdict, text):
		# 0801Update: 修复了一个可能导致二进制文件封包编码错误的问题
		for item in tdict:
			if str(text).__contains__(str(item)):
				return True
		return False

	def get_mac_address(self):
		# 思路来源：https://blog.csdn.net/dongfuguo/article/details/72863950
		# return the MAC address of the computer
		for (k,v) in net_if_addrs().items():
			for item in v:
				addr = item[1]
				if '-' in addr and len(addr) == 17:
					return str(addr).replace('-','').upper()
		return ''


	def random_captcha(self):
		return str(random.randint(1000,9999))

	def renew_ip(self):
		time.sleep(2)
		print("Linux版本已取消网络自修复功能，等待连接重试...")
		time.sleep(2)

	def get_my_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			s.connect(('8.8.8.8', 80))
			ip = s.getsockname()[0]
		finally:
			s.close()
		return ip

	def get_jsversion(self):
		t = self.login(self.url_jsversion,{},method="GET")
		r = re.compile(r'jsVersion=\'(.*)\'')
		rlst = r.findall(t)
		if len(rlst) == 0:
			return "3.3.2"
		return str(r.findall(t)[0])

	def command_login(self):
		# 0801Update: 全新适配新校园网登录模式
		resptext = self.do_login()
		if self.check_str(self.str_check, resptext):
			print("用户:" + self.usr + " 登录成功！")
		else:   # 0801Update: 第一次登录可能返回AC错误，重试即可
			time.sleep(2)
			resptext = self.do_login()
			if self.check_str(self.str_check, resptext):
				print("用户:" + self.usr + " 登录成功！")
			else:   # 0801Update: 两次尝试失败，再重新刷新IP再试
				self.renew_ip()
				resptext = self.do_login()
				if self.check_str(self.str_check, resptext):
					print("用户:" + self.usr + " 登录成功！")
				else:
					print("您的用户名/密码可能输入有误，请检查后重试！")
					print("[注意] 新校园网可能会遇到链接问题，您也可以选择等待5分钟后重新尝试")

	def do_login(self):
		params = {'user_account': ',0,' + self.usr,
		          'user_password': self.pwd,
		          'c': 'Portal',
		          'a': 'login',
		          'callback': 'dr1003',
		          'login_method': '1',
		          'wlan_user_ip': self.ipaddr,
		          'wlan_user_ipv6': '',
		          'wlan_user_mac': self.macaddr,
		          'wlan_ac_ip': '',
		          'wlan_ac_name': 'jlh_me60',
		          'jsVersion': self.jsversion,
		          'v': self.random_captcha()}
		return self.login(self.url_login, data=params, method='GET')

	def command_logout(self):
		# 0801Update: 2019暑假更新后，注销功能可能无法正常使用
		params = {'c': 'Portal',
		          'a': 'logout',
		          'callback': '1003',
		          'user_account': "drcom",
		          'user_password': "123456",
		          'login_method': '1',
		          'ac_logout': '0',
		          'register_mode': '1',
		          'wlan_user_ip': self.ipaddr,
		          'wlan_user_ipv6': '',
		          'wlan_user_mac': self.macaddr,
		          'wlan_vlan_id': '0',
		          'wlan_ac_ip': '',
		          'wlan_ac_name': 'jlh_me60',
		          'jsVersion': self.jsversion,
		          'v': self.random_captcha()}
		header_logout = self.headers
		header_logout['Referer'] = 'http://202.119.25.2/a79.htm?UserIP={}&wlanacname=jlh_me60'.format(self.ipaddr)
		resptext = self.login(self.url_login, data=params, method="GET", header=header_logout)
		if self.check_str(self.str_check, resptext):
			print("用户:" + self.usr + " 已注销登录！")
		else:
			print("注销登录失败，用户可能还未登录...")

	def check_status(self):
		params = {'callback': 'dr1002',
		          'v': self.random_captcha()}
		resptext = self.login(self.url_checkstatus, data=params, method='GET')
		if self.check_str(self.str_status, resptext):
			return True
		else:
			return False

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

	def login(self, htmlUrl='', data={}, method='POST', header={}):
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		time.sleep(0.2)  # 防止封IP
		if htmlUrl == '':
			htmlUrl = self.url_login
		htmlUrl_get = list()
		for (k, v) in data.items():
			htmlUrl_get.append(k + "=" + str(v))
		htmlUrl_get = "&".join(htmlUrl_get)
		if header == '':
			header = self.headers
		try:
			if method.upper() == 'GET':
				r = self.session.get(htmlUrl + "?" + htmlUrl_get, headers=header, data=data, verify=False)
			else:
				r = self.session.post(htmlUrl, headers=header, data=data, verify=False)
		except:
			self.renew_ip()
			try:
				if method.upper() == 'GET':
					r = self.session.get(htmlUrl + "?" + htmlUrl_get, headers=header, data=data)
				else:
					r = self.session.post(htmlUrl, headers=header, data=data)
			except:
				print("网络连接无法修复，请检查配置或等待一会后重试！")
				return ""
		# 0801Update: 新版校园网使用字符串判断状态前应过滤一些字符串
		rt = r.text
		for fil in self.str_filter:
			rt = rt.replace(fil,'')
		return rt