from pyecharts import Map, Geo, Bar, Page, Line, Pie
import data_analyze
import pandas,os
import settings

'''
生成各种报表
'''
# ------------------------------ 工具
def sort_dic(dic, sortField, ascending = False):
    data = pandas.DataFrame(dic)
    data = data.sort_values(sortField, ascending = ascending)
    ret_dic = data.to_dict('list')
    return ret_dic

def render(echarts, name):
    echarts.render(path=os.path.join(name+".html"))

# ------------------------------ 生成

def gen_table(tableName, keys, values):
    bar = Bar(tableName)
    bar.add(tableName, keys, values, is_label_show=True, xaxis_rotate=30, is_datazoom_show=True)
    #render(bar, tableName)
    return bar

def gen_pie(tableName, attr, values):
    pie = Pie(tableName)
    pie.add(name=tableName, attr=attr, value=values, is_label_show = True)
    #render(pie, tableName)
    return pie

def run():
    page = Page()

    data_dict = data_analyze.textAndImg()
    table = gen_pie("朋友圈图文比例", ["图片数量", "文本数量"], [data_dict["img_count"], data_dict["text_count"]])
    page.add(table)

    data_dict = data_analyze.countPerMonth()
    table = gen_table("各月发表数量", data_dict["date"], data_dict["weekDay"], )
    page.add(table)

    render(page, "综合分析") # 整合成一个html


if __name__ == "__main__":
    run()