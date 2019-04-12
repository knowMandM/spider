from pyecharts import Map, Geo, Bar, Page, Line
import data_analyze
import my_log as log
import pandas,os
import settings
'''
生成各种报表
'''

# ------------------------------ 工具
def cvtSalaryArr(salaries):
    def cvtSalary(x):
        return round(x,1)*1000
    return list(map(cvtSalary, salaries))

def sort_dic(dic, sortField, ascending = False):
    data = pandas.DataFrame(dic)
    data = data.sort_values(sortField, ascending = ascending)
    ret_dic = data.to_dict('list')
    return ret_dic

def render(echarts, name):
    echarts.render(path=os.path.join(settings.WORK_PATH, "html", name+".html"))

# ------------------------------ 生成
# 生成中国地图，显示各省（直辖市）职位数量
def china_map(province, jobcount):
    provice = province
    values = jobcount

    map = Map("各省职位分布", width=1200, height=600)
    map.add("", provice, values, visual_range=[100, 8000],  maptype='china', is_visualmap=True,
        visual_text_color='#000', is_map_simbol_show=False,is_label_show = False)
    map.show_config()
    render(map, "各省职位分布")
    return map

# 生成各市职位数量,薪水柱形图
def city_jobcount(cities, jobcount, salaries):
    bar = Bar("毕业后该去哪", "北京无论是职位数量还是薪水,都是领先其他城市")
    bar.add("职位数量", cities[:10], jobcount[:10], is_label_show=True)
    bar.add("平均薪资(元/月)", cities[:10], cvtSalaryArr(salaries[:10]), is_label_show=True)
    render(bar, "城市-职位数量工资")
    return bar

def stage_jobcount(stages, jobcount, salaries):
    bar = Bar("各成长阶段职位数量,平均薪资")
    bar.add("职位数量", stages, jobcount, is_label_show=True)
    bar.add("平均薪资", stages, cvtSalaryArr(salaries), is_label_show=True)
    render(bar, "成长阶段")
    return bar

def salary_distribution(qujian, jobcount):
    def cvt_qujian(x):
        x = x.replace(",", "-").replace("(","").replace("]","K").replace(" ", "")
        return x
    bar = Bar("薪资分布")
    bar.add("职位数量", list(map(cvt_qujian, qujian)), jobcount, is_label_show=True)
    render(bar, "薪资分布")
    return bar

def secondType_joibcount_salary(secondType, jobcount, salaries):
    bar = Bar("各互联网职位的职位数量,平均薪资")
    bar.add("职位数量", secondType[:15], jobcount[:15], is_label_show=True,xaxis_rotate=30, yaxis_rotate=30)
    bar.add("平均薪资", secondType[:15], cvtSalaryArr(salaries[:15]), is_label_show=True, xaxis_rotate=30, yaxis_rotate=30)
    render(bar, "职位的职位数量,平均薪资")
    return bar

def industry_jobcount_salary(industry, jobcount):
    bar = Bar("互联网最热20个方向")
    bar.add("职位数量", industry[:20], jobcount[:20], is_label_show=True,xaxis_rotate=30)
    render(bar, "互联网最热20个方向")
    return bar

def language_jobcount(language, job_count):
    bar = Bar("编程语言需求量")
    bar.add("职位数量", language, job_count, is_label_show=True,xaxis_rotate=30)
    render(bar, "编程语言需求量")
    return bar

def language_salary(language, salaries):
    bar = Bar("编程语言薪资")
    bar.add("平均薪资", language, cvtSalaryArr(salaries), is_label_show=True,xaxis_rotate=30)
    render(bar, "编程语言薪资")
    return bar

def experience_jobcount(experience, job_count):
    bar = Bar("经验对应职位数量")
    bar.add("职位数量", experience, job_count, is_label_show=True,xaxis_rotate=30)
    render(bar, "经验对应职位数量")
    return bar

def experience_salary(experience, salaries):
    bar = Bar("经验对应薪资")
    bar.add("平均薪资", experience, cvtSalaryArr(salaries), is_label_show=True,xaxis_rotate=30)
    render(bar, "经验对应薪资")
    return bar

def gen_table(tableName, x_name, keys, values):
    bar = Bar(tableName)
    bar.add(x_name, keys, values, is_label_show=True, xaxis_rotate=30)
    render(bar, tableName)
    return bar

def cities_experience_salary(list_data):
    tablename = "各城市经验增长对应薪资增长"
    line = Line(tablename)
    for dic in list_data:
        line.add(dic["city"], dic["workYear"], cvtSalaryArr(dic["salary"]))
    render(line, "各城市经验增长对应薪资增长")
    return line

def run():
    page = Page()

    data_dict = data_analyze.provincejobcount()
    table = china_map(data_dict["keys"], data_dict["values"])
    page.add(table)

    data_dict = data_analyze.cityjobcount_salary()
    table = city_jobcount(data_dict["keys"], data_dict["job_count"], data_dict["salary"])
    page.add(table)

    data_dict = data_analyze.financeStage_jobcount_salary()
    table = stage_jobcount(data_dict["keys"], data_dict["job_count"], data_dict["salary"])
    page.add(table)

    data_dict = data_analyze.salary_distribution()
    table = salary_distribution(data_dict["keys"], data_dict["job_count"])
    page.add(table)
    
    data_dict = data_analyze.secondType_jobcount_salary()
    table = secondType_joibcount_salary(data_dict["keys"], data_dict["job_count"], data_dict["salary"])
    page.add(table)
    
    data_dict = data_analyze.industry_jobcount_salary()
    table = industry_jobcount_salary(data_dict["keys"], data_dict["job_count"])
    page.add(table)
    
    data_dict = data_analyze.language_jobcount_salary()
    table = language_jobcount(data_dict["keys"], data_dict["job_count"])
    page.add(table)
    
    data_dict = sort_dic(data_dict, "salary")
    table = language_salary(data_dict["keys"], data_dict["salary"])
    page.add(table)
    
    data_dict = data_analyze.experience_jobcount_salary()
    table = experience_jobcount(data_dict["keys"], data_dict["job_count"])
    page.add(table)
    
    data_dict = sort_dic(data_dict, "salary")
    table = experience_salary(data_dict["keys"], data_dict["salary"])
    page.add(table)
    
    data_dict = data_analyze.education_jobcount_salary()
    table = gen_table("学历需求量", "职位数量", data_dict["keys"], data_dict["job_count"])
    page.add(table)
    
    data_dict = sort_dic(data_dict, "salary")
    table = gen_table("学历薪资", "平均薪资", data_dict["keys"], cvtSalaryArr(data_dict["salary"]))
    page.add(table)
    
    list_data = data_analyze.cities_exp_salary()
    table = cities_experience_salary(list_data)
    page.add(table)
    
    data_dict = data_analyze.company_salary()
    table = gen_table("各大公司平均薪资", "平均薪资", data_dict["keys"], cvtSalaryArr(data_dict["salary"]))
    page.add(table)
    render(page, "综合分析") # 整合成一个html


if __name__ == "__main__":
    run()