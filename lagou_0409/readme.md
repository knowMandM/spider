
# 一. 如果需要运行项目,按以下方式操作
### 1. 安装python3.5.1
```
安装包文件夹下有
```

### 2. 解压项目,并安装依赖

```c
1.cmd中cd到项目目录
2.pip install -r requirements.txt -i https://pypi.doubanio.com/simple/
```

### 3. 配置mysql用户名密码
```
打开setting.py 修改以下配置项
# mysql数据库配置
mysql_user = "root"
mysql_passwd = "123456"
mysql_dbname = "mydb"
```

### 4. 爬取拉勾网数据（ajax数据）
```
运行main.py
```

