import csv,os
import json
import redis_dup
from my_log import log
import settings

'''
ajax数据写入器
'''
# 表数据路径
csv_path = settings.DATA_FILE_PATH
# 表头
headers = ["companyId",
            "positionLables",
            "industryLables",
            "businessZones",
            "financeStage",
            "positionAdvantage",
            "companySize",
            "companyLabelList",
            "publisherId",
            "district",
            "score",
            "positionId",
            "positionName",
            "createTime",
            "workYear",
            "education",
            "city",
            "companyLogo",
            "jobNature",
            "salary",
            "approve",
            "industryField",
            "companyShortName",
            "formatCreateTime",
            "longitude",
            "latitude",
            "hitags",
            "resumeProcessRate",
            "resumeProcessDay",
            "imState",
            "lastLogin",
            "explain",
            "plus",
            "pcShow",
            "appShow",
            "deliver",
            "gradeDescription",
            "promotionScoreExplain",
            "firstType",
            "secondType",
            "isSchoolJob",
            "subwayline",
            "stationname",
            "linestaion",
            "thirdType",
            "skillLables",
            "companyFullName",
            "adWord",
            "mycity",
            "language",
            "gm"]

datas = []
total_count = 0

def writeCsv():
    global datas
    global total_count
    exist = os.path.exists(csv_path)
    with open(csv_path, 'a+', newline='') as f:
        # 标头在这里传入，作为第一行数据
        try:
            writer = csv.DictWriter(f, headers)
            if not exist:
                writer.writeheader()

            # 还可以写入多行
            writer.writerows(datas)
            total_count += len(datas)
            #log("写入：", len(datas), "  总计：", total_count)
        except Exception as e:
            log(e)
        finally:
            datas = []

#工具函数, 事后误删redis时可以用这个重新插入, 平时没啥用
def readCsvAndInsertRedisKey():
    with open(csv_path, 'r+', newline='') as f:
        try:
            rows = csv.DictReader(f, headers)
            for row in rows:
                print(row["companyFullName"] + row["positionName"])
                redis_dup.isExist(row["companyFullName"] + row["positionName"])
        except Exception as e:
            log(e)
    
# 分析json字符串，读取各字段信息
def fillData(jsonObj, language, city, gm):
    data = {}
    for fieldName in headers:
        if fieldName in jsonObj:
            data[fieldName] = jsonObj[fieldName]
    data["mycity"] = city
    data["language"] = language
    data["gm"] = gm

    if not redis_dup.isExist(data["companyFullName"] + data["positionName"]):
        datas.append(data)
    else:
        try:
            print("data exist:", data["companyFullName"] + data["positionName"])
        except Exception as e:
            print(e)

# 对外接口，外部调用这个函数即可写csv文件
def writeInfo(jsonList, language, city, gm):
    for result in jsonList:
        fillData(result, language, city, gm)
        writeCsv()
    log("总写入：", total_count)
    

if __name__ == "__main__":
    pass
    # readCsvAndInsertRedisKey()