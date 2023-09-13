import re
import requests
import json
from pyinstrument import Profiler
class Crawler():
    def __init__(self):
        self.keyword = ''
        self.total = 0
        self.currentotal = 0
        self.abv = []
        self.headers = {
            "cookie": "buvid3=7525DDCC-965F-5188-3274-C80DE462731034982infoc; b_nut=1679374034; _uuid=38B76C72-5864-107F2-F8B9-A9A3106DEDC9936134infoc; rpdid=|(u))kkYuuu~0J'uY~mJmuY)R; i-wanna-go-back=-1; header_theme_version=CLOSE; nostalgia_conf=-1; LIVE_BUVID=AUTO5616796523942780; buvid_fp_plain=undefined; CURRENT_PID=ed69d7f0-ca4e-11ed-b3e8-c97d9d419989; hit-dyn-v2=1; CURRENT_BLACKGAP=0; is-2022-channel=1; b_ut=5; FEED_LIVE_VERSION=V8; DedeUserID=486122667; DedeUserID__ckMd5=59131a86ff7f0152; buvid4=137828BD-AC2E-5CE0-6845-AA5757D9CAA907361-022112423-%2FxwqHe8zHTWeS3ozfRBFRw%3D%3D; CURRENT_QUALITY=80; fingerprint=52def87be9e86d0db5e22fc20e932427; buvid_fp=588ac5aee9614692a2d385c5781595fb; CURRENT_FNVAL=4048; SESSDATA=32021daa%2C1709471055%2C58842%2A9248VgMsX43i4C0r5gyQapTYXRCk53ZakCAX6Zrb56zXEJD76bBYa2JZdOeqKZ8FBwblMrYwAAQwA; bili_jct=dd9485d247a7a628d97580461d231698; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQxNzgyNTgsImlhdCI6MTY5MzkxOTA1OCwicGx0IjotMX0.8FB1XJwhq_IT-VZHfXrJLc4EdBs0EqF259qi_m0QUCs; bili_ticket_expires=1694178258; hit-new-style-dyn=1; home_feed_column=5; browser_resolution=1854-937; bp_video_offset_486122667=838590663763165268; b_lsid=9173C3D8_18A705F53AC; PVID=2; sid=fwcnd4gm",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
        }
        self.acid = []

    def search(self,keyword,total):
        self.keyword = keyword
        self.total = total

    def get_bvid(self): #获取bvid号
        totalpage = (int(self.total) // 42) + 1  # 因为哔哩哔哩一页有42个视频，要爬300个视频就要爬8页
        # print(totalpage)
        page = 1  # 当前页数
        while page <= totalpage:
            url = f'https://api.bilibili.com/x/web-interface/wbi/search/type?page={page}&page_size=42&keyword={self.keyword}&search_type=video'
            # print(url)
            data_bvid = requests.get(url=url, headers=self.headers)
            # print(data.json())
            ABV = re.findall('BV..........', data_bvid.text)  # 寻找符合bv号的数据，格式是BV加11个字母数字
            page += 1
            # i = 0
            # for bv in ABV:
            #     print(bv)
            #     i+=1
            # print(i)
            self.abv += ABV  # 防止覆盖，将这次循环爬到的bvid列表加入类里的bvid列表中保存。

    def get_cid(self):  # 通过bvid获取cid号
        for bvid in self.abv:
            url = f'https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp//'
            # print(url)
            data_cid = requests.get(url=url, headers=self.headers) #
            dirt = json.loads(data_cid.text)
            cid = dirt['data'][0]['cid']
            # print(cid)
            self.acid.append(cid)
            self.currentotal += 1  # 统计当前已经爬取到的cid号，因为只能一页一页的爬，只能是42的整数倍个。
            if int(self.currentotal) > int(self.total):  # 只保留输入的要保留的cid数量。
                break
            # i = 0
            # for cid in self.acid:
            #     print(bv)
            #     i+=1
            # print(i)

    def get_danmaku(self):  # 通过cid获取弹幕
        for cid in self.acid:
            url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
            data_danmuku = requests.get(url=url,headers=self.headers)
            data_danmuku.encoding = 'utf-8'
            # print(data_danmuku.text)
            # danmuku = BeautifulSoup(data_danmuku.text)
            danmuku_list = re.findall('<d p=".*?">(.*?)</d>' ,data_danmuku.text)  # 使用正则表达式来爬取弹幕。
            # print(danmuku_list)
            f = open('danmuku.txt', mode='a', encoding="utf-8")  # 写入一个叫做danmuku.txt的文件，使用追加模式。
            for index in danmuku_list:
                content = index
                f.write(content)
                f.write("\n")  # 追加一个换行号

if __name__ == '__main__':
        c = Crawler()
        c.search('日本核污染水排海','300')
        profiler = Profiler()
        profiler.start()
        c.get_bvid()
        print(c.abv)
        c.get_cid()
        print(c.acid)
        c.get_danmaku()
        profiler.stop()
        profiler.print()

