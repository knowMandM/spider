
oriHeader = '''
Accept: application/json
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 62
Content-Type: application/x-www-form-urlencoded
Cookie: bid=3l4ZQTkZpMQ; ll="118172"; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=D641EB067D86A7D6B3E6CF1ED1D925523|6a905ef32430799b038ed18c433803ea; douban-fav-remind=1; ps=y; douban-profile-remind=1; _pk_ref.100001.2fad=%5B%22%22%2C%22%22%2C1554963654%2C%22https%3A%2F%2Fsec.douban.com%2Fb%3Fr%3Dhttps%253A%252F%252Fmovie.douban.com%252Fexplore%22%5D; _pk_ses.100001.2fad=*; ap_v=0,6.0; _pk_id.100001.2fad=89de7f0b3acb3595.1554714280.3.1554964873.1554955892.; login_start_time=1554964875300
Host: accounts.douban.com
Origin: https://accounts.douban.com
Referer: https://accounts.douban.com/passport/login?source=movie
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
X-Requested-With: XMLHttpRequest'''

priCookies = '''
bid=HDPuKg2jkHA; ps=y; ll="118200"; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=DAA377EA02893468B1D32C8D1FB019456|0690659b978fc22ae31677c24aa61172; dbcl2="194825171:CPMr/pzeNYY"; ck=khv2; __utma=30149280.1318472213.1554909456.1554909456.1554988717.2; __utmb=30149280.0.10.1554988717; __utmc=30149280; __utmz=30149280.1554988717.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login'''

def printDict(d):
    print("{")
    for key, value in d.items():
        print(r"    r'{}':r'{}',".format(key, value))
    print("}")

def convertHeaders(headerFromChrome):
    lines = headerFromChrome.split('\n')
    ret = {}
    for line in lines:
        if ": " in line:
            key_value = line.split(": ")
            key = key_value[0]
            value = key_value[1]
            ret[str.strip(key)] = str.strip(value)
    # printDict(ret)
    return ret

def convertCookies(cookieFromChrome):
    pairList = cookieFromChrome.split(";")
    ret = {}
    for pair in pairList:
        if "=" in pair:
            key_value = pair.split("=")
            key = key_value[0]
            value = key_value[1]
            ret[str.strip(key)] = str.strip(value)
    # printDict(ret)
    return ret

def convertData(data):
    data = data.replace('\"', "")
    return convertHeaders(data)

def convertParam(data):
    return convertHeaders(data)

if __name__ == "__main__":
    
    convertHeaders('''
        cateId: 2001313
        cateOrbreedName: 
        collectDate: "2019-04-16"
        marketType: area
        pageNum: 2
        pageSize: 10
        ''')
    #convertCookies(priCookies)