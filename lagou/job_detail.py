from bs4 import BeautifulSoup as bs
import settings
import pandas
import requests
import time

'''
爬拉勾网职位详情页, 生成词云的数据来源
'''
class LagouJobDetail():
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

    # 根据职位的positionid，组成待爬详情页的url
    def generateUrl(self, positionID):
        return "https://www.lagou.com/jobs/{ID}.html".format(ID = positionID)

    # 从详情页html数据中分析出职位详情信息
    def analyze_job_detail(self, markup):
        bs_data = bs(markup)

        div_list = bs_data.find_all("div")
        for div in div_list:
            if "job-detail" in div.get("class", []):
                return div.get_text()

    # 反爬
    def updateCookies(self):
        self.session = requests.Session()
        self.session.get(self.url_cookie, headers = self.headers, timeout=3)
        r = requests.utils.dict_from_cookiejar(self.session.cookies) #获取 LGRID
        r["user_trace_token"] = r["user_trace_token"]
        r["LGSID"] = r["user_trace_token"]
        r["LGUID"] = r["user_trace_token"]
        self.cookies.update(r)
        time.sleep(2)

    # 打开详情页
    def getJobDetail(self, positionID):
        self.updateCookies()
        response = self.session.get(url = self.generateUrl(positionID), headers = self.headers, cookies = self.cookies)
        response.encoding = response.apparent_encoding
        return response.text

    # 功能入口
    def run(self, listPositionID, outputFilePath):
        with open(outputFilePath, "w+", encoding="utf-8") as output_file:
            count = 0
            for positionID in listPositionID:
                try:
                    output_file.write(jobdetail.analyze_job_detail(jobdetail.getJobDetail(positionID)))
                    output_file.flush()
                    count += 1
                    print(count)
                except Exception as e:
                    print(e)
        

if __name__ == "__main__":
    jobdetail = LagouJobDetail()
    jobdetail.run(settings.javapositionids, settings.javaJobDetailfile)
    jobdetail.run(settings.hulianwangpositionids, settings.hulianwangJobDetailfile)
