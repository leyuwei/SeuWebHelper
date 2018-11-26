# -*- coding:utf-8 -*-
# Compiled with Python 3.7

import seuhelper
from seuhelper import *

def main():
	helper = seuhelper("220170000", "123456")

	# 单次操作：登录账户
	# helper.command_login()

	# 单次操作：注销账户
	# helper.command_logout()

	# 部署：10分钟检测一次登录状态，注销的话就自动重登
	# helper.keep_alive(10)

if __name__ == "__main__":
	main()