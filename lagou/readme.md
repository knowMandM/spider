# 一. 最终页面
```
html/拉勾网数据分析.html
```

# 二. 如果需要运行项目,按以下方式操作
### 1. 安装python3.5.1
```
安装包文件夹下有
```

### 2. 解压项目,并安装依赖

```c
1.cmd中cd到项目目录
2.pip install -r requirements.txt -i https://pypi.doubanio.com/simple/
```

### 3. 安装redis
```
安装包在包里，安装教程 http://www.runoob.com/redis/redis-install.html
```

### 4. 爬取拉勾网数据（ajax数据）
```
运行main.py
```

### 5. 爬取拉勾网数据（详情页）
```
运行job_detail.py
```
### 6. 规整数据
- ajax数据 没有省份信息，需要在excel中匹配出来
- 薪资规整
- 解析出行业

### 7. 生成图表
```
运行data_analyze/gen_table.py
```
### 8. 生成词云
```
运行data_analyze/gen_word_cloud.py
```

### 9. 将词云图片整合进html
```
需要懂html... 直接拿我做好的"拉勾网数据分析.html"吧,就是最终成果了
```


