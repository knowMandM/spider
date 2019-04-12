import pandas
import numpy
import sys,os
sys.path.append(".")
import settings

df = pandas.read_csv(settings.DATA_FILE_PATH, encoding="gbk")

# 解析工资（15k-17k 转为 16）
def calc_salary(lagou_salary):
    lagou_salary = lagou_salary.replace('以上','').replace('以下','')
    splitsalary = lagou_salary.split('-')
    min = splitsalary[0]
    max = min
    if len(splitsalary) > 1:
        max = splitsalary[1]
    avg = (int(min.upper().replace('K','')) + int(max.upper().replace('K',''))) / 2
    return avg

# 预处理，工资转换成平均工资数字
for i in range(df["salary"].size):
    df.loc[i, "salary"] = calc_salary(df["salary"][i])
    print(df["salary"][i])

df.to_csv(settings.DATA_FILE_PATH_PROCESSED)