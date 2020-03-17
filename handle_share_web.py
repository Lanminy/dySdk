#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree

from handle_db import handle_get_task

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H7088O24GU71RXVD"
proxyPass = "1D60C3D7538C9DEE"


def handle_decode(input_data):
    # 匹配icon font
    regex_list = [
        {'name': [' &#xe603; ', ' &#xe60d; ', ' &#xe616; '], 'value': 0},
        {'name': [' &#xe602; ', ' &#xe60e; ', ' &#xe618; '], 'value': 1},
        {'name': [' &#xe605; ', ' &#xe610; ', ' &#xe617; '], 'value': 2},
        {'name': [' &#xe604; ', ' &#xe611; ', ' &#xe61a; '], 'value': 3},
        {'name': [' &#xe606; ', ' &#xe60c; ', ' &#xe619; '], 'value': 4},
        {'name': [' &#xe607; ', ' &#xe60f; ', ' &#xe61b; '], 'value': 5},
        {'name': [' &#xe608; ', ' &#xe612; ', ' &#xe61f; '], 'value': 6},
        {'name': [' &#xe60a; ', ' &#xe613; ', ' &#xe61c; '], 'value': 7},
        {'name': [' &#xe60b; ', ' &#xe614; ', ' &#xe61d; '], 'value': 8},
        {'name': [' &#xe609; ', ' &#xe615; ', ' &#xe61e; '], 'value': 9},
    ]
    #
    for i1 in regex_list:
        for i2 in i1['name']:
            input_data = re.sub(i2, str(i1['value']), input_data)  # 把正确value替换到自定义字体上

    html = etree.HTML(input_data)
    douyin_info = {}

    # 获取昵称
    douyin_info['nick_name'] = \
    html.xpath("//div[@class='personal-card']/div[@class='info1']//p[@class='nickname']/text()")[0]
    # 获取抖音ID
    douyin_id = ''.join(html.xpath("//div[@class='personal-card']/div[@class='info1']/p[@class='shortid']/text()"))
    douyin_id = douyin_id.replace('抖音ID：', '').replace(' ', '')
    i_id = ''.join(html.xpath("//div[@class='personal-card']/div[@class='info1']/p[@class='shortid']/i/text()"))
    douyin_info['douyin_id'] = str(douyin_id) + str(i_id)
    # douyin_info['douyin_id'] = re.sub(search_douyin_str, '', html.xpath("//div[@class='personal-card']/div[@class='info1']//p[@class='nickname']/text()")[0]).strip() + douyin_id
    # 职位类型
    try:
        douyin_info['job'] = html.xpath(
            "//div[@class='personal-card']/div[@class='info2']/div[@class='verify-info']/span[@class='info']/text()")[
            0].strip()
    except:
        pass
    # 描述
    douyin_info['describe'] = \
    html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='signature']/text()")[0].replace('\n', ',')
    # 关注
    douyin_info['follow_count'] = ''.join(html.xpath(
        "//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='focus block']//i/text()"))
    # 粉丝
    fans_value = ''.join(html.xpath(
        "//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='follower block']//i[@class='icon iconfont follow-num']/text()"))
    unit = html.xpath(
        "//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='follower block']/span[@class='num']/text()")
    if unit[-1].strip() == 'w':
        douyin_info['fans_str'] = str(float(fans_value) / 10) + 'w'
        fans_count = douyin_info['fans_str'][:-1]
        fans_count = float(fans_count)
        fans_count = fans_count * 10000
        douyin_info['fans_count'] = fans_count
    else:
        douyin_info['fans_str'] = fans_value
        douyin_info['fans_count'] = fans_value
    # 点赞
    like = ''.join(html.xpath(
        "//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='liked-num block']//i[@class='icon iconfont follow-num']/text()"))
    unit = html.xpath(
        "//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='liked-num block']/span[@class='num']/text()")
    if unit[-1].strip() == 'w':
        douyin_info['like_str'] = str(float(like) / 10) + 'w'
        like_count = douyin_info['like_str'][:-1]
        like_count = float(like_count)
        like_count = like_count * 10000
        douyin_info['like_count'] = like_count
    else:
        douyin_info['like_str'] = like
        douyin_info['like_count'] = like

    # 作品
    worko_count = ''.join(html.xpath("//div[@class='video-tab']/div/div[1]//i/text()"))
    douyin_info['work_count'] = worko_count

    return douyin_info


def handle_douyin_web_share(task):
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    share_web_url = 'https://www.iesdouyin.com/share/user/{}'.format(task['share_id'])
    print(share_web_url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    share_web_response = requests.get(share_web_url, headers=headers, proxies=proxies)
    douyin_info = handle_decode(share_web_response.text)
    print(douyin_info)


if __name__ == '__main__':
    while True:
        task = handle_get_task()
        handle_douyin_web_share(task)