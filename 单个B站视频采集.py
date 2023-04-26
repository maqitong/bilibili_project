"""
爬虫思路
一、数据来源分析
    爬什么？ B站视频、标题
    去哪爬？ url =  ‘https://www.bilibili.com/video/BV1zk4y1J7Ph/’
        静态的还是动态的
        静态 我在源代码里搜索标题，发现有json格式的数据==>json在Script标签里

二、爬虫代码实现
    发送请求
    数据获取
    数据解析
    数据保存
"""
import requests
import re
import json
import os  #  系统模块，让pytho操作windows系统

def get_html(url, headers):
    try:
        resp = requests.get(url=url, headers=headers)
        resp.encoding = 'utf-8'
        resp.raise_for_status()  # 自动触发崩溃
        return resp.text
    except:
        return ''



def parse_html(html):
    """
    解析数据有几种方法：
    1、解析（string --> object）

    2、搜索（re正则）

    """

    js_code = re.findall(r'<script>window.__playinfo__=(.*?)</script>',html,re.S)[0]  # (匹配规则、字符串、re.S所有字符串包括换行符) .:匹配任意字符不包括换行符 *:出现0次或多次 *?:非贪婪即匹配到想要的就终止。？?本意出现0/1次
    js_dict = json.loads(js_code)  #  json.loads()将json字符串转换为python字典

    # 解析视频的URL
    data = js_dict['data']
    dash = data['dash']
    video = dash['video']
    video_base_url = video[0]['base_url']

    # 解析音频的URL
    audio = dash['audio']
    audio_base_url = audio[0]['base_url']


    # 解析标题
    title = re.findall(r'<title.*?>(.*?)</title>', html,re.S)[0]

    data_dict = {
        'title' : title,
        'video_base_url' : video_base_url,
        'audio_base_url' : audio_base_url,
    }

    return data_dict

def save_data(data, headers):
    # 如果没有文件夹我就创建一个
    base_filename = './视频/'
    if not os.path.exists(base_filename):
        os.mkdir(base_filename)

    video = get_content(url=data['video_base_url'], headers=headers)
    audio = get_content(url=data['audio_base_url'], headers=headers)

    filename = base_filename + f'{data["title"]}/'
    if not os.path.exists(filename):
        os.mkdir(filename)

    with open(filename + 'video.mp4','ab+',) as f:
        f.write(video)
    with open(filename + 'audio.mp3', 'ab+', ) as f:
        f.write(audio)

    combine(filename)

def get_content(url, headers):
    try:
        resp = requests.get(url=url, headers=headers)
        resp.raise_for_status()

        return resp.content   #  content二进制数据，text文本数据，json() json数据
    except:
        return ''

def combine(filename):
        os.system(f'ffmpeg -i {filename}video.mp4 -i {filename}audio.mp3 -c:v copy -c:a aac -strict experimental {filename}output.mp4')
"""
功能：让python执行cmd命令
参数：命令字符串
返回值：无


"""

"""
exists()
功能：判断一个文件在不在
参数：路径
返回值：布尔
"""


def main():
    url = 'https://www.bilibili.com/video/BV1Kv4y1J7No/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
        'referer': 'https://www.bilibili.com/',
    }

    html = get_html(url, headers)
    if not html:
        print('获取失败')

    data = parse_html(html)

    if not data:
        print('解析失败')

    save_data(data, headers)
if __name__ == '__main__':
    main()