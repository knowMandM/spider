import requests,json
import convert_cookies
# 用于快速验证的

headers = '''
            Accept: application/json, text/plain, */*
            Content-Type: application/json
            Origin: http://m.cnhnb.com
            Referer: http://m.cnhnb.com/hangqing/blm/
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
            '''
cookies = ''''''

data    = '''
        cateId: 2001313
        cateOrbreedName: 
        collectDate: "2019-04-16"
        marketType: area
        pageNum: 2
        pageSize: 10
        '''
params  = '''
'''
url = "https://gateway.cnhnb.com/monk/market/marketNew/v2/getMarketBreedByArea"

httpType = "post" # post 或 get
dataType = "json" # form 或 json


# ----------------- 以下不用动
def run():
    global headers, cookies, data, params

    headers = convert_cookies.convertHeaders(headers)
    cookies = convert_cookies.convertCookies(cookies)
    data = convert_cookies.convertData(data)
    params = convert_cookies.convertData(params)

    if dataType == 'json':
        data = json.dumps(data)

    response = {}
    if httpType == 'post':
        response = requests.post(url, headers = headers, data=data, params=params, cookies=cookies)
    elif  httpType == 'get':
        response = requests.get(url, headers = headers, params=params, cookies=cookies)
    else:
        print("httpType{} not support".format(httpType))

    print(response.text)


if __name__ == "__main__":
    run()