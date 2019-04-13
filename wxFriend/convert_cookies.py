
oriHeader = '''
                        Accept: application/json, text/javascript, */*; q=0.01
                        Accept-Encoding: gzip, deflate, br
                        Accept-Language: zh-CN,zh;q=0.9
                        Connection: keep-alive
                        Content-Type: text
                        Host: chushu.la
                        Referer: https://chushu.la/book/chushula-491790819
                        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
                        X-Requested-With: XMLHttpRequest
                    '''

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
    printDict(ret)
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
    printDict(ret)
    return ret

if __name__ == "__main__":
    convertHeaders(oriHeader)
    convertCookies(priCookies)