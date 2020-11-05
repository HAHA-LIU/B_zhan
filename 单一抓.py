import requests
import os

url = 'http://upos-sz-mirrorcosb.bilivideo.com/upgcxcode/19/03/176670319/176670319-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1604485164&gen=playurl&os=cosbbv&oi=3733188690&trid=6c0992eb87df4348825b8c61f2ff330du&platform=pc&upsig=55385072f4000c3d2febc86bd4f1082d&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=2,3&agrr=1&logo=40000000'

headers = {
    'referer': 'https://www.bilibili.com/video/BV1WJ411e76L?from=search',
    'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

info = requests.get(url=url, headers=headers)
# total_size = int(info.headers['content-length'])

path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'video'
if not os.path.exists(path):
    os.makedirs(path)

with open(f'{path}{os.sep}1.mp4', 'wb') as f:
    f.write(info.content)



