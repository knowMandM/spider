import requests
import time, os, sys
import json
import convert_cookies
from items import WxItem
import csv_writer, gen_table

'''
爬自己的所有微信朋友圈动态
'''
class SpiderWx():
    def __init__(self):
        self.session = requests.Session()
        self.cookies = {
            'Hm_lvt_a64b0c58cf35c32b2f7fd256b188b238': str(int(time.time()))
        }
        self.page_info_headers = convert_cookies.convertHeaders('''
                        Accept: application/json, text/javascript, */*; q=0.01
                        Content-Type: text
                        Referer: https://chushu.la/book/chushula-865104491
                        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
                        X-Requested-With: XMLHttpRequest
                    ''')
        
        self.data_headers = convert_cookies.convertHeaders('''
                        Accept: application/json, text/javascript, */*; q=0.01
                        Content-Type: application/json
                        Origin: https://chushu.la
                        Referer: https://chushu.la/book/chushula-865104491
                        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
                        X-Requested-With: XMLHttpRequest
                    ''')
        self.url_page_info = "https://chushu.la/api/book/chushula-865104491?isAjax=1"      # 获取页数的 url
        self.url_data = "https://chushu.la/api/book/wx/chushula-865104491/pages?isAjax=1"  # 获取朋友圈动态的 url
        self.query_count = 0

    # 更新cookie
    def updateCookies(self):
        r = {}
        r["Hm_lvt_a64b0c58cf35c32b2f7fd256b188b238"] = str(int(time.time()))
        self.cookies.update(r)
        #time.sleep(1)

    # 查询共多少页信息, 
    def get_wxPageInfo(self):
        self.updateCookies()

        response = self.session.get(url = self.url_page_info, headers = self.page_info_headers, cookies = self.cookies)
        decodedJson = json.loads(response.text)
        print(decodedJson)
        return self.constructPayLoadArray(decodedJson)

    # 组好 post 参数数组
    def constructPayLoadArray(self, decodedJson):
        pageCount = len(decodedJson["book"]["catalogs"])
        catalog = decodedJson["book"]["catalogs"]
        payLoadArr = []
        for i in range(pageCount):
            payLoadArr.append(
                                {   
                                    'index': 3+i,
                                    'month': catalog[i]["month"],
                                    'type': "year_month",
                                    'value': "v_{}{}".format(catalog[i]["year"], catalog[i]["month"]),
                                    'year': catalog[i]["year"]
                                }
                            )
        return payLoadArr


    # post爬取朋友圈动态
    def _getDataImpl(self, params, data):
        print(data)
        self.updateCookies()

        response = self.session.post(url = self.url_data, headers = self.data_headers, cookies = self.cookies, data = json.dumps(data))

        response.encoding = response.apparent_encoding
        decodedJson = json.loads(response.text)
        if "pages" in decodedJson:
            self.writeInfo(decodedJson)
        else:
            print(decodedJson)
            def callback():
                return self._getDataImpl(params, data)
            self.onBlocked(callback)

    # 根据返回的json解析出数据
    def writeInfo(self, decodedJson):
        import re
        def replaceByRe(srcStr, reRule, replaceStr):
            pattern = re.compile(reRule)
            return re.sub(pattern, replaceStr, srcStr)

        def filter_emoji(desstr,restr=''):
            '''
            过滤表情
            '''
            try:
                co = re.compile(u'[\U00010000-\U0010ffff]')
            except re.error:
                co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
            return co.sub(restr, desstr)

        for pageInfo in decodedJson["pages"]:
            if pageInfo["type"] == "weixin_month_page":
                continue

            item = WxItem()
            item.date       = pageInfo["data"]["dateText"][:-3]
            item.text       = replaceByRe(' '.join([ ''.join([para["data"] for para in x['rows']]) for x in pageInfo["data"]["paras"]]), r'<img\s.*>', '')
            item.imgCount   = len(pageInfo["data"]["imgs"])
            item.imgs       = repr([x["src"] for x in pageInfo["data"]["imgs"]])
            item.weekDay    = pageInfo["data"]["dateOfWeek"]
            print(item.to_dict())
            csv_writer.appendData("wxinfo.csv", item.headers(), item.to_dict())


    # ip被封时,等待10分钟重试
    def onBlocked(self, callBack = None):
        time.sleep(60 * 10)
        if(callBack):
            callBack()

    # 遍历post参数发起查询
    def post_wxInfo(self, payLoadArr):
        for payLoad in payLoadArr:
            self._getDataImpl("", payLoad)
    
    # 功能入口
    def run(self):
        # 清理数据
        csv_writer.clearData("wxinfo.csv")
        # 爬数据并落到csv文件中
        self.post_wxInfo(
            self.get_wxPageInfo()
            )
        # 数据分析，生成表
        gen_table.run()

if __name__ == '__main__':
    SpiderWx().run()