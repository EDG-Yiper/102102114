import jieba
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import wordcloud
import csv #使用excel保存

file=open(r"danmuku.txt",encoding ="utf-8")  # 打开要制作词云的文本
text=file.read()  # 读取文本
file.close()  # 关闭文件
wordlist = list(jieba.cut(text))  # 进行分词处理
# print(type(wordlist))
wordlist = [word for word in wordlist if len(word)>1]  # 该条主要是为了排除一个字符以下的词，没有这条文本将会分出都是单字。

word = " ".join(wordlist)  # 该条将分好的列表词，转为空格分隔的字符串

# 停用词处理
stopfile=open(r"stopwords.txt",encoding ="utf-8")  # 读取停用词
stopword=stopfile.read().split("\n")  # 读取的停用词都带"\n"需要进行删除
stopfile.close()  # 关闭文档


# 词云处理
imgpath=np.array(Image.open( r"D:\table\v2-7941a51789bf94c6d67c32c383ee6a48_r.jpg"))  # 词云背景图片
wc = wordcloud.WordCloud( font_path='C:\Windows\Fonts\STKAITI.TTF',
                          background_color='white',
                          mask=imgpath,
                          max_words=200,
                          max_font_size=100,
                          width=900,
                          height=900,
                          scale=17,
                          random_state=5,stopwords=stopword)
wc.generate(word)#传入需画词云图的文本
#对词云进行展示
plt.imshow(wc)

plt.axis("off")# 隐藏图像坐标轴
plt.savefig(r"bar_img.png", dpi=400)#保存图片
plt.show()# 展示图片
plt.close()#关闭图片

#词频统计
Excel = open("danmuku.csv", 'w', newline='')  # 打开表格文件，若表格文件不存在则创建
writ = csv.writer(Excel)  # 创建一个csv的writer对象用于写每一行内容
writ.writerow(['名称', '出现次数'])  # 写表格表头
counts = {}  # 创建一个字典，用于对词出现次数的统计，键表示词，值表示对应的次数
for word in wordlist:
    if len(word) <= 1:
        continue
    else:
        counts[word] = counts.get(word, 0) + 1  # 在字典中查询若该字返回次数加一
item = list(counts.items())  # 将字典转化为列表格式
item.sort(key=lambda x: x[1], reverse=True)
for i in range(20):
    writ.writerow(item[i])  # 将前20名写入表格

