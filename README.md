# SeuWebHelper
东南大学校内无线局域网自动登录脚本，防电脑断链，永久保持在线

# Requirements
请使用Python3.5以上版本

# Tutorial
安装`requirements.txt`中的依赖包后，请编辑`main.py`中的内容，将其中的用户名密码替换成自己的，然后根据实际情况取消下面几行控制代码的注释

举例：每15分钟维护一次登录状态，发现被踢出后，自动重登录。

	helper = seuhelper("220170000", "123456")

	# 单次操作：登录账户
	# helper.command_login()

	# 单次操作：注销账户
	# helper.command_logout()

	# 部署：10分钟检测一次登录状态，注销的话就自动重登
	# helper.keep_alive(10)
  
