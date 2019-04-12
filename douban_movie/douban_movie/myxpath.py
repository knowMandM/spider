
def myXpath(response, sXpath):
    #print(response.xpath(sXpath).extract_first())
    return response.xpath(sXpath).extract_first()