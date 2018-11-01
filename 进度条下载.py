import requests
import os
import re
import codecs
from contextlib import closing


def url_open(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def page_open(page_url):
    html = url_open(page_url)
    return html

def find_mp3(html):
    pattern = r'data-url="(.*?)"'
    mp3_url = re.findall(pattern, str(html), re.S)
    return mp3_url


def data_title(html):
    pattern = r'data-title="(.*?)"'
    title = re.findall(pattern, str(html), re.S)
    return title


def save_mp3s(urls,file_path):
    with closing(requests.get(urls, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        data_count = 0
        with open(file_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r 文件下载进度：%d%%(%d/%d) - %s" %(now_jd, data_count, content_size, file_path), end=" ")




def download_mp3(folder, pages):
    ur = 'http://livemusical.kz/artist'
    url = ur + '/' + str(folder)
    for i in range(pages):
        page_num = int(i) + 1
        page_url = url + '/' + str(page_num)
        html = page_open(page_url)
        mp3_url = find_mp3(html)
        title = data_title(html)
        for urls,file_path in zip(mp3_url,title):
            urls = 'http://livemusical.kz%s' % urls
            file_path = "G:\\music/%s.mp3" % file_path
            save_mp3s(urls,file_path)
            print(page_num)


if __name__ == '__main__':
    folder = input("请输入歌手名: ")
    pages = input("请输入要下载的页数: ")
    download_mp3(str(folder), int(pages))
