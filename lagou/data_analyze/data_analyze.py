import pandas
import numpy
import sys,os
sys.path.append(".")
import settings
'''
分析ajax数据，为生成图表提供数据支持
'''

# 判断字符串中是否含有中文
def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

# 展开技能标签
def getUnwindSkillData():
    def formatSkillName(skill):
        skill = skill.lower()
        mp = {
            "c" : "c/c++",
            "c++" : "c/c++",
            "js" : "javascript/html",
            "html5" : "javascript/html",
            "html" : "javascript/html",
            "web前端" : "javascript/html",
            "javascript" : "javascript/html",
            "j2ee" : "java",
            "go" : "golang",
            "linux":"linux/unix",
        }
        if skill in mp:
            skill = mp[skill]
        return skill

    skillDf = pandas.DataFrame([])
    if os.path.exists(settings.DATA_FILE_PATH_MID):
        skillDf = pandas.read_csv(settings.DATA_FILE_PATH_MID)
    else:
        skillDf["companyId"] = df["companyId"]
        skillDf["salary"] = df["salary"]
        skillDf["skillLables"] = df["skillLables"]

        size = df["skillLables"].size
        count = 0
        for i in range(size):
            labels = df["skillLables"][i]
            lebelList = eval(labels)
            for label in lebelList:
                skillDf = skillDf.append([{
                            "companyId" : df["companyId"][i],
                            "salary" : df["salary"][i],
                            "skillLables" : formatSkillName(label)
                        }])
                count += 1
                print(count)
        skillDf.to_csv(settings.DATA_FILE_PATH_MID)
    return skillDf

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

df = pandas.read_csv(settings.DATA_FILE_PATH_PROCESSED, encoding="gbk")

# 分析各省职位数量
def provincejobcount():
    ret_dict = {}
    ret_dict["keys"]   = [x for x in df["province"].value_counts().index]
    ret_dict["values"] = [x for x in df["province"].value_counts().values]
    return ret_dict


''' 
    function : analyze_jobcount_salary
    description : 用来统计各个纬度对应的职位数量和平均工资
    parameter: 
        sIndex # 统计维度
    return
        dict{
            "keys"      : []  # 维度
            "job_count" : []  # 职位数量
            "salary"    : []  # 平均工资
        }
'''
def analyze_jobcount_salary(sIndex, df = df, sortField = "job_count", ascending=False):
    ret_dict = {}
    dict_data = df.pivot_table(index=sIndex, values=["companyId","salary"], aggfunc=[len, numpy.mean])
    ret_df = pandas.DataFrame({
        sIndex : [x for x in dict_data.index],
        "job_count" : [x for x in dict_data["len"]["companyId"]],
        "salary" : [x for x in dict_data["mean"]["salary"]]
    })

    ret_df = ret_df.sort_values(sortField, ascending=ascending)
    print(ret_df.head(100))
    ret_dict["keys"] = [str(x) for x in ret_df[sIndex]]
    ret_dict["job_count"] = [x for x in ret_df["job_count"].values]
    ret_dict["salary"] = [x for x in ret_df["salary"].values]
    return ret_dict

# 按城市的维度分析职位和工资
def cityjobcount_salary():
    return analyze_jobcount_salary("city")

# 按发展阶段分析
def financeStage_jobcount_salary():
    return analyze_jobcount_salary("financeStage", sortField = "financeStage", ascending = True)

# 工资区间分析
def salary_distribution():
    seris = pandas.cut(df["salary"], [0,5,10,20,30,50,100,200])
    df["salary_distribution"] = seris.astype("object")
    #print(df.pivot_table(index="salary_distribution", values="salary"))
    return analyze_jobcount_salary("salary_distribution")

# 各互联网职位的职位数量,平均薪资
def secondType_jobcount_salary():
    return analyze_jobcount_salary("secondType")

# 最热方向
def industry_jobcount_salary():
    return analyze_jobcount_salary("industry")

# 编程语言分析
def language_jobcount_salary():
    dic = analyze_jobcount_salary("skillLables", df = getUnwindSkillData())
    ddf = pandas.DataFrame(dic)
    ddf = ddf.loc[ddf['keys'].str.contains(r"^((?!\[).)+", regex=True) , ["keys", "job_count","salary"]]   #过滤[
    ddf = ddf.loc[ddf['keys'].str.contains(r"^[\x01-\x7f]*$", regex=True) , ["keys", "job_count","salary"]] #过滤中文

    return ddf.head(10).to_dict("list")


# 经验对应职位数量和工资
def experience_jobcount_salary():
    return analyze_jobcount_salary("workYear")

# 学历对应职位数量和工资
def education_jobcount_salary():
    return analyze_jobcount_salary("education")

# 各城市不同经验对应工资子函数
def city_experience_salary(city):
    ddf = df.pivot_table(index=["city", "workYear"], values=["salary"])
    ddf = ddf.loc[(city)].sort_values("salary")
    return ddf.reset_index().to_dict("list")

# 各城市不同经验对应工资
def cities_exp_salary():
    lst = ["杭州", "北京", "上海", "深圳", "广州"]
    dic_list = []
    for city in lst:
        ret = city_experience_salary(city)
        ret["city"] = city
        dic_list.append(ret)
    return dic_list

# 各大公司薪水
def company_salary():
    dataframe = pandas.DataFrame(analyze_jobcount_salary("companyShortName"))
    return dataframe.head(20).to_dict("list")














