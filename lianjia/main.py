import requests
import convert_cookies
from lxml import etree
from orm_items import lianjia_info
from faker import Factory
from mysql_mgr import mysqlMgr
import redis_dup
import time

fake = Factory.create()

class LianJiaSpider:
    code2city = {
        'ly'       : "龙岩",
        'quanzhou' : "泉州",
        'xm'       : "厦门",
        'zhangzhou': "漳州"
    }
    
    # ----- 流程函数
    def start_requests(self):
        for cityCode in self.code2city:
            self.request_city(cityCode)
        print("------- crawl finished. -------")
        return True

    def parse(self, response, citycode):
        html = etree.HTML(response.text)

        loupan_names    = html.xpath(r"//ul[@class='resblock-list-wrapper']//a[@class='name ']/text()")
        resblock_types  = html.xpath(r"//ul[@class='resblock-list-wrapper']//span[@class='resblock-type']/text()")
        sale_status     = html.xpath(r"//ul[@class='resblock-list-wrapper']//span[@class='sale-status']/text()")
        addrs           = html.xpath(r"//ul[@class='resblock-list-wrapper']//div[@class='resblock-location']")
        addrs           = [x.xpath('string(.)').replace(' ', '').replace('\r', '').replace('\n', '') for x in addrs]
        prices          = html.xpath(r"//ul[@class='resblock-list-wrapper']//span[@class='number']/text()")
        units           = html.xpath(r"//ul[@class='resblock-list-wrapper']//span[@class='desc']/text()")

        if len(prices) > len(units):
            for i in range(len(prices)):
                if prices[i] == '价格待定': # 处理有些楼盘没有价格的问题
                    units.insert(i, "")
                    prices[i] = -1

        for i in range(len(loupan_names)):
            item = lianjia_info()
            item.name           = loupan_names[i]
            item.city           = self.code2city[citycode]
            item.loupan_type    = resblock_types[i]
            item.sale_status    = sale_status[i]
            item.address        = addrs[i]
            item.price          = prices[i]
            item.units          = units[i]
            item.crawl_time     = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # 重复的不插入
            unique_key = '|'.join([item.name, item.city, item.loupan_type, item.address])
            if not redis_dup.isExist('lianjia', unique_key):
                self.store_data(item)
            else:
                print(unique_key, "has exist.")

    def store_data(self, item):
        mysqlMgr.insertValue(item)

    # ----- 功能函数
    def request_city_by_page(self, citycode, page=1):
        url = "https://{city}.fang.lianjia.com/loupan/pg{page}".format(
            city=citycode, page=page)
        headers = convert_cookies.convertHeaders('''
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
            Accept-Encoding: gzip, deflate, br
            Accept-Language: zh-CN,zh;q=0.9
            Cache-Control: max-age=0
            Connection: keep-alive
            Host: quanzhou.fang.lianjia.com
            Upgrade-Insecure-Requests: 1
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
        ''')
        host = "{}.fang.lianjia.com".format(citycode)
        headers["Host"] = host
        headers["User-Agent"] = fake.user_agent()

        print("url:", url)
        response = requests.get(url, headers=headers)
        time.sleep(0.2)
        return response

    def get_page_num(self, citycode):
        response = self.request_city_by_page(citycode)
        if response.status_code == 200:
            html = etree.HTML(response.text)
            count = html.xpath(r"//div[@class='resblock-have-find']//span[@class='value']/text()")[0]
            return int(count) // 10 + 1
        return 0

    def request_city(self, cityCode):
        page_num = self.get_page_num(cityCode)
        for i in range(page_num):
            response = self.request_city_by_page(cityCode, i+1)
            if response.status_code == 200:
                self.parse(response, cityCode)

    def run(self):
        self.start_requests()

if __name__ == "__main__":
    LianJiaSpider().run()


