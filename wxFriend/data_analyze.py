import pandas
import numpy
import sys,os
sys.path.append(".")
import settings

'''
分析ajax数据，为生成图表提供数据支持
'''
df = pandas.read_csv(settings.CSV_PATH, encoding="utf-8")
df.reset_index
# 图文比例
def textAndImg():
    ret_dict = {}
    ret_dict["img_count"]  = df["imgCount"].sum()
    ret_dict["text_count"] = len(df.loc[df["text"] != ""]["text"])
    return ret_dict

# 每月动态数量
def countPerMonth():
    dff = df.loc[df["text"].notnull()]
    resDf = dff.pivot_table(index = "date", values="weekDay", aggfunc=len)
    print(resDf)
    return resDf.reset_index().to_dict("list")




