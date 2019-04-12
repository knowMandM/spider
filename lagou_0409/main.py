import requests
import time, os, sys
import json
import settings as search_condition
import csv
import write_mysql
from my_log import log

'''
爬拉勾网ajax接口的职位信息
'''
class SpiderLagou():
    def __init__(self):
        self.session = None
        self.cookies = {
                        'X_MIDDLE_TOKEN': '797bc148d133274a162ba797a6875817',
                        'JSESSIONID': 'ABAAABAAAIAACBI03F33A375F98E05C5108D4D742A34114',
                        '_ga': 'GA1.2.1912257997.1548059451',
                        '_gat': '1',
                        'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1548059451',
                        'user_trace_token': '20190121163050-dbd72da2-1d56-11e9-8927-525400f775ce',
                        'LGSID': '20190121163050-dbd72f67-1d56-11e9-8927-525400f775ce',
                        'PRE_UTM': '',
                        'PRE_HOST': '',
                        'PRE_SITE': '',
                        'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F%3F_from_mid%3D1',
                        'LGUID': '20190121163050-dbd73128-1d56-11e9-8927-525400f775ce',
                        '_gid': 'GA1.2.1194828713.1548059451',
                        'index_location_city': '%E5%85%A8%E5%9B%BD',
                        'TG-TRACK-CODE': 'index_hotjob',
                        'LGRID': '20190121163142-fb0cc9c0-1d56-11e9-8928-525400f775ce',
                        'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1548059503',
                        'SEARCH_ID': '86ed37f5d8da417dafb53aa25cd6fbc0',
                        }
        self.headers = {
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.lagou.com',
                        'Referer': 'https://www.lagou.com/jobs/list_java',
                        'X-Anit-Forge-Code': '0',
                        'X-Anit-Forge-Token': 'None',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Connection': 'keep-alive',
                        'Cache-Control': 'max-age=0',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                        #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                        }
        self.url_cookie = "https://www.lagou.com/jobs/list_C++"
        self.url_data = "https://www.lagou.com/jobs/positionAjax.json"
        self.query_count = 0

    def updateCookies(self):
        self.session = requests.Session()
        self.session.get(self.url_cookie, headers = self.headers, timeout=3)
        r = requests.utils.dict_from_cookiejar(self.session.cookies) #获取 LGRID
        r["user_trace_token"] = r["user_trace_token"]
        r["LGSID"] = r["user_trace_token"]
        r["LGUID"] = r["user_trace_token"]
        self.cookies.update(r)
        time.sleep(2)

    # 查询总共多少职位
    def getJobCountInCity(self, sSearch = '', sCity = '', gm = ''):
        param = {
            "px":"default",
            "city" : sCity,
            "needAddtionalResult" : 'false',
        }
        if len(gm) > 0:
            param["gm"] = gm

        data = {
            'first': 'true',
            'pn': 1,
            'kd': sSearch
        }

        jsonObj = self._getDataImpl(param, data)
        return jsonObj["content"]["positionResult"]["totalCount"]

    # 真正执行查询的接口
    def _getDataImpl(self, params, data):
        self.updateCookies()

        response = self.session.post(url = self.url_data, headers = self.headers, params = params, cookies = self.cookies, data = data)

        response.encoding = response.apparent_encoding
        decodedJson = json.loads(response.text)
        if "content" in decodedJson:
            return decodedJson
        else:
            print(decodedJson)
            def callback():
                return self._getDataImpl(params, data)
            self.onBlocked(callback)

    # ip被封时,等待10分钟重试
    def onBlocked(self, callBack = None):
        log("IP被封, 10分钟后重试")
        time.sleep(60 * 10)
        if(callBack):
            callBack()

    # 查询职位数据
    def getDataByCity(self, sSearch = '', sCity = '', gm = "", totalJobCount = 0):
        param = {
            "px":"new",
            "gm": gm,
            "city" : sCity,
            "needAddtionalResult" : 'false',
        }
        
        log(sCity, sSearch, gm, "共:", totalJobCount)
        x = 0
        while x < (totalJobCount // 15 + 1):
            x += 1
            self.query_count += 1

            data = {
            'first': 'true',
            'pn': str(x),
            'kd': sSearch
            }
            log(sSearch, sCity, gm, "第", x, "页")
            jsonObj = self._getDataImpl(param, data)
            if jsonObj["content"]["positionResult"]['resultSize'] <= 0:
                log("没有记录")
                continue
            # 写mysql数据库
            write_mysql.insertValues(jsonObj["content"]["positionResult"]["result"])
            if jsonObj["content"]["positionResult"]['resultSize'] < 15:
                return log("没有下一页了，跳出")
    # 功能入口
    def run(self):
        for city in search_condition.cityArr:
            jobCount = self.getJobCountInCity("", city)
            if(jobCount > 0):
                self.getDataByCity("", sCity = city, totalJobCount=jobCount)
            else:
                log(city, "没有", "", "相关职位，跳过。")
    

if __name__ == '__main__':
    SpiderLagou().run()