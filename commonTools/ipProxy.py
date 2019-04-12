import requests
import random

def getOneIpProxy():
    iplist = eval(requests.get("http://127.0.0.1:5010/get_all").text)

    ipPort = None
    if len(iplist) > 0:
        ipPort = random.choice(iplist)
        return ipPort
