# -*- coding:utf-8 -*- 
# author: LIUWENYU
# datetime: 2020/11/2 15:39
# describe:
import requests
from fake_useragent import UserAgent
from lxml import etree
import re
import time
import os
import subprocess

class Bilib():
    def __init__(self,search_name=None):
        """
        :param search_name: 查询关键词
        其他参数说明：
        keyword：关键词 例如：西游记
        order: totalrank 综合排序，click 最多点击，pubdate 最新发布，dm 最多弹幕，stow 最多收藏
        duration：0 全部时长，1 10分钟以下，2 10-30分钟，3 30-60分钟，4 60分钟以上
        tids_1: 0 全部分区，1 动画，13 番剧，167 国创，3 音乐，129 舞蹈。。等等 这个选项有点多
        page：1 第一页，2 第二页
        eg：https://search.bilibili.com/video?keyword=西游记&order=totalrank&duration=1&tids_1=0&page=1
        """
        # 关键字
        self.search_name = search_name
        # 请求头
        self.headers = {"User-Agent": UserAgent().random}
        # 下载视频请求头
        self.downloadVideoHeaders = {
            'referer': 'https://www.bilibili.com/video/BV1WJ411e76L?from=search',
            'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        self.link_list = []

    # 获取网页源码
    def get_html(self,url):
        result_url = requests.get(url=url,headers=self.headers)
        if result_url.status_code == 200:
            return result_url.text
        else:
            print('Get Html Code is False:%s,没有查询到相关视频' % result_url.status_code)
            return

    # 获取视频页数
    def get_page_count(self,html):
        # 对网页数据进行解析，提取需要的视频链接
        result_etree = etree.HTML(html)
        page_num = result_etree.xpath('//li[contains(@class,"page-item last")]/button/text()')
        page_num = re.findall(r'\d+',page_num[0])[0]
        return page_num

    # 获取视频地址
    def get_link(self,html):
        if not html: return
        # 对网页数据进行解析，提取需要的视频链接
        result_etree = etree.HTML(html)
        link_list_result = result_etree.xpath('//*[@id="video-list"]/ul/li/a/@href')
        for item in link_list_result:
            self.link_list.append(item)
        return self.link_list

    # 根据视频地址，获取视频
    def get_video(self,video_count,page_num_t):
        # 存放路径
        path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'video'
        if not os.path.exists(path):
            os.makedirs(path)

        # 合并后的视频位置
        path_new = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'videoNew'
        if not os.path.exists(path_new):
            os.makedirs(path_new)

        # 下载数量
        if 0 < video_count < page_num_t * 20:
            for i in range(len(self.link_list))[:video_count]:
                result_video = requests.get(url='http:' + self.link_list[i], headers=self.headers).text
                video_url = re.findall(r'"base_url":"(.*?)"', result_video)  # 匹配视频，音频地址
                video_name = etree.HTML(result_video).xpath('//*[@id="viewbox_report"]/h1/span/text()')
                video_name = '-'.join(re.findall(r'[\w]+', video_name[0]))  # 视频名称
                print(f'{video_name}---下载中...')
                # 存视频
                info_s = requests.get(url=video_url[0], headers=self.downloadVideoHeaders).content
                with open(f'{path}{os.sep}{video_name}1.mp4', 'wb') as f:
                    f.write(info_s)
                # 存音频
                info_y = requests.get(url=video_url[-1], headers=self.downloadVideoHeaders).content
                with open(f'{path}{os.sep}{video_name}2.mp4', 'wb') as f:
                    f.write(info_y)
                time.sleep(1)
                filename = f'{path_new}{os.sep}{video_name}.mp4'
                yin_video = f'{path}{os.sep}{video_name}1.mp4'
                shi_video = f'{path}{os.sep}{video_name}2.mp4'
                # 合并音视频
                self.video_add_mp4(filename,yin_video,shi_video)
                print(f'{video_name}---下载完成...')

        # 下载全部视频
        if video_count == 0:
            for i in self.link_list:
                result_video = requests.get(url='http:' + self.link_list[i],headers=self.headers).text
                video_url = re.findall(r'"base_url":"(.*?)"',result_video)  # 匹配视频，音频地址
                video_name = etree.HTML(result_video).xpath('//*[@id="viewbox_report"]/h1/span/text()')
                video_name = '-'.join(re.findall(r'[\w]+', video_name[0]))  # 视频名称
                print(video_name)
                # 存视频
                info_s = requests.get(url=video_url[0], headers=self.downloadVideoHeaders).content
                with open(f'{path}{os.sep}{video_name}1.mp4', 'wb') as f:
                    f.write(info_s)
                # 存音频
                info_y = requests.get(url=video_url[-1], headers=self.downloadVideoHeaders).content
                with open(f'{path}{os.sep}{video_name}2.mp4', 'wb') as f:
                    f.write(info_y)

    # 视频 + 音频 合并
    def video_add_mp4(self,filename,yin_video,shi_videop):
        cmd = f'F:\\FFmpeg\\bin\\ffmpeg -i {yin_video} -i {shi_videop} -acodec copy -vcodec copy {filename}'
        print(cmd)
        subprocess.call(cmd, shell=True)

    def main(self):
        while True:
            search_name = input('请输入查询视频关键字：')
            # search_name = '西游记'
            if not search_name:
                continue
            break

        # 页数
        url = f"https://search.bilibili.com/video?keyword={search_name}&order=totalrank&duration=1&tids_1=0"
        html = self.get_html(url=url)
        page_num = self.get_page_count(html)
        print(f'相关视频有{page_num}页,每页视频大概20个')
        while True:
            page_num_t = int(input('请选择下载几页：'))
            if page_num_t > int(page_num):
                print('输入页码有误，请重新输入')
                continue
            break

        # 视频数量
        while True:
            print('数量规则：0<数量<20*页数，0表示选择页数的全部视频')
            video_count = int(input('请输入下载视频数量：'))
            if video_count < 0 or video_count > page_num_t *20 :
                print('输入数量有误，请重新输入')
                continue
            break

        # 地址
        links = ''
        for i in range(1,page_num_t+1):
            url_t = f"https://search.bilibili.com/video?keyword={search_name}&order=totalrank&duration=1&tids_1=0&page={i}"
            print(url_t)
            html = self.get_html(url=url_t)
            links = self.get_link(html)
            print(f'第{i}页,视频地址获取完成')
            time.sleep(2)   # 睡眠一会，访问频率过快，会被认为网络爬虫，将IP地址关进小黑屋
        print(f'总共获取视频地址数量{len(links)}')

        # 下载视频
        self.get_video(video_count,page_num_t)

if __name__ == '__main__':
    b = Bilib()
    b.main()

