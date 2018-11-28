# -*- coding:utf-8 -*-
# Compiled with Python 3.7

import seuhelper
from seuhelper import *
from sys import argv

def main():

	# 1128 增加命令行参数模式支持

	if argv.__len__() == 1:
		# 不输入任何参数时，脚本可按照自定义代码执行
		helper = seuhelper("220170000", "123456")
		# 单次操作：登录账户
		# helper.command_login()
		# 单次操作：注销账户
		# helper.command_logout()
		# 部署：10分钟检测一次登录状态，注销的话就自动重登
		# helper.keep_alive(10)
	elif argv.__len__() == 3:
		helper = seuhelper(argv[1], argv[2])
		helper.keep_alive(10)
	elif argv.__len__() == 4:
		helper = seuhelper(argv[1], argv[2])
		helper.keep_alive(int(argv[3]))
	else:
		print("请正确输入命令行参数\n输入格式：python main.py [用户名] [密码] [检测间隔(分钟)]*\n检测间隔为可选参数，不输入时默认为10分钟")

if __name__ == "__main__":
	main()