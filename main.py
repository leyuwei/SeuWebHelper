# -*- coding:utf-8 -*-
# Compiled with Python 3.7

import seuhelper
import ctypes
from seuhelper import *
from sys import argv

def main():

	# 0613 更新五参数输入时隐藏运行窗口功能
	# 0322 适配校园网新SSL错误提示
	# 0322 修复校园网更新导致的登录失效问题
	# 1228 增加Invalid_Location错误检测
	# 1228 增加对校园网https安全接口的自动识别
	# 1220 增加网络连接故障时的自动修复
	# 1204 增加用户输入参数支持
	# 1204 修复切换登录用户却仍然使用上一用户的BUG
	# 1128 增加命令行参数模式支持

	if argv.__len__() == 1:
		# 不输入任何参数时，脚本会接受外部输入
		usr = input("请输入用户名： ")
		pwd = input("请输入密码： ")
		interval = input("请输入检测间隔(分钟)： ")
		helper = seuhelper(usr.strip(), pwd.strip())
		helper.command_logout()
		helper.keep_alive(int(interval))
		# 单次操作：登录账户
		# helper.command_login()
		# 单次操作：注销账户
		# helper.command_logout()
		# 部署：10分钟检测一次登录状态，注销的话就自动重登
		# helper.keep_alive(10)
	elif argv.__len__() == 3:
		helper = seuhelper(argv[1], argv[2])
		helper.command_logout()
		helper.keep_alive(10)
	elif argv.__len__() == 4:
		helper = seuhelper(argv[1], argv[2])
		helper.command_logout()
		helper.keep_alive(int(argv[3]))
	elif argv.__len__() >= 5:
		print("已准备隐藏运行窗口...")
		print("如需关闭请在任务管理器中结束python.exe进程！")
		time.sleep(5)
		whnd = ctypes.windll.kernel32.GetConsoleWindow()
		if whnd != 0:
			ctypes.windll.user32.ShowWindow(whnd, 0)
			ctypes.windll.kernel32.CloseHandle(whnd)
		helper = seuhelper(argv[1], argv[2])
		helper.command_logout()
		helper.keep_alive(int(argv[3]))
	else:
		print("请正确输入命令行参数\n输入格式：python main.py [用户名] [密码] [检测间隔(分钟)]*\n检测间隔为可选参数，不输入时默认为10分钟")

if __name__ == "__main__":
	main()