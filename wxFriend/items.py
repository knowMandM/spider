import base_item
from base_item import *

# 自定义的微信数据结构
class WxItem(BaseItem):
    date = String()
    imgCount = Integer()
    weekDay = String()
    text = String()
    imgs = String()

    def __init__(self):
        self.date = "1"
        self.text = "2"
        self.imgCount = 0
        self.imgs = "3"
        self.weekDay = "4"


if __name__ == "__main__":
    #use Example
    print(type(repr([x for x in [1]])))
    print(repr([x for x in [1]]))
    import csv_writer
    a = WxItem()
    print(a.headers())
    print(a.to_dict())
    print(a.values())
    csv_writer.clearData("a.csv")
    csv_writer.appendData("a.csv", a.headers(), [a.to_dict(),  a.to_dict()])