import os
'''
这是项目配置
'''

# 工作目录
WORK_PATH = os.getcwd()

# 日志文件路径
LOG_PATH = os.path.join(WORK_PATH, "log", "lagou.log")

# 搜索的城市
cityArr = ['福州']

# mysql数据库配置
mysql_user = "root"
mysql_passwd = "123456"
mysql_dbname = "mydb"