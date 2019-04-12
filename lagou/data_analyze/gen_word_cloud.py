
# -*- coding: utf-8 -*-
import pandas
import matplotlib.pyplot as plt
import pickle
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
import codecs, sys
sys.path.append(".")
import settings, os

'''
词云生成
'''
oriJavaFilePath = os.path.join(settings.WORK_PATH, "csv", "javaJobDetail.txt")
oriHulianwangFilePath = os.path.join(settings.WORK_PATH, "csv", "hulianwangJobDetail.txt")

out_hulianwang_cloud_pic = os.path.join(settings.WORK_PATH, "html", "hulianwang_wc.png")
out_java_cloud_pic = os.path.join(settings.WORK_PATH, "html", "java_wc.png")

processedFilePath = os.path.join(settings.WORK_PATH, "csv", "temp.txt")
background_img = os.path.join(settings.WORK_PATH, "data_analyze", "cloud.jpg")
color_img = os.path.join(settings.WORK_PATH, "data_analyze", "color.jpg")

def gen_word_cloud(srcFile, outputPic):
    # 规整字符串,以免大小写认为是不同的词
    def format(str):
        return str.capitalize()
    # 判断是否含有中文
    def check_not_contain_chinese(check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return False
        return True

    #第一次运行程序时将分好的词存入文件
    text = ''
    with open(srcFile, encoding = "utf-8") as fin:
        for line in fin.readlines():
            line = line.strip('\n')
            text += ' '.join(list(map(format, list(filter(check_not_contain_chinese, jieba.lcut(line))))))
            text += ' '
    fout = open(processedFilePath,'wb')
    pickle.dump(text,fout)
    fout.close()

    #ps = pandas.Series(text.split())
    #ps.value_counts().to_csv("频率.csv")

    # 直接从文件读取数据
    fr = open(processedFilePath,'rb')
    text = pickle.load(fr)

    backgroud_Image = plt.imread(background_img)
    wc = WordCloud( background_color = 'white',    # 设置背景颜色
                    mask = None,        # 设置背景图片
                    max_words = 150,            # 设置最大现实的字数
                    stopwords = STOPWORDS,        # 设置停用词
                    font_path = r'C:\Windows\Fonts\msyh.ttc',# 设置字体格式，如不设置显示不了中文
                    max_font_size = 100,            # 设置字体最大值
                    random_state = 30,            # 设置有多少种随机生成状态，即有多少种配色方案
                    width=600, height= 400,
                    collocations=False
                    )
    wc.generate(text)
    image_colors = ImageColorGenerator(plt.imread(color_img))
    wc.recolor(color_func = image_colors)
    wc.to_file(outputPic)

# 生成java词云
gen_word_cloud(oriJavaFilePath, out_java_cloud_pic)
# 生成互联网词云
gen_word_cloud(oriHulianwangFilePath, out_hulianwang_cloud_pic)