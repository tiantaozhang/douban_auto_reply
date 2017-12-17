# -*- coding: utf8 -*-

"""
auto up
"""

from config.dev import *
import requests
from lxml import etree
import urllib2
import pytesseract
try:
    import Image
except:
    from PIL import Image
import os
from io import BytesIO
import sys


headers = {'Host': 'www.douban.com', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0', 'Content-Type': 'application/x-www-form-urlencoded'}

headers_get = {'Host': 'www.douban.com', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'}


cookies = {
    'cookie': '_vwo_uuid_v2=827F611908AF587B6F63F957ACE209D3|1b8d8440cd49c10bb2424a0bd3fe13aa; ps=y; ue="327468120@qq.com"; dbcl2="58423576:ZoB2oEe1PTc"; ck=1Rkx; ct=y; bid=vpe0lFyQ26Q; _ga=GA1.2.1038127754.1479557262; _gid=GA1.2.1767544224.1512223410; ap=1; __utmt=1; push_noty_num=0; push_doumail_num=0; __utma=30149280.1038127754.1479557262.1512225624.1512290369.49; __utmb=30149280.57.5.1512291992450; __utmc=30149280; __utmz=30149280.1512223400.47.19.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.5842'
}

def reply(cookies={}):
    for url in SPECIAL_TOPICS:
        reply_url = url + 'add_comment#last'
        payload = {
            'ck': cookies.get('ck'),
            'rv_comment': 'upupup',
            'start': 0,
        }
        print cookies
        print payload
        r = requests.post(reply_url, data=payload, cookies=cookies)
        # print r.status_code, r.content


def dir_path(pre, name):
    return './tmp/%s%s' % (pre, name)

def verification_code(fimg, name):
    gray = fimg.convert('L')        # 灰度处理
    gray.save(dir_path('gray', name))
    bw = gray.point(lambda x: 0 if x < 55 else 255, '1')     # 阀值
    bw.show()
    bw.save(dir_path('thresholded', name))
    code = pytesseract.image_to_string(bw)
    if not code:
        print "please input verify code:"
        code = sys.stdin.readline().strip('\n')
    return code


def verification_code_from_path(img_path):
    fimg = Image.open(img_path)
    name = os.path.basename(img_path)
    code = verification_code(fimg, name)
    return code


def login():
    # get first, avoid captcha image
    response = requests.get('https://www.douban.com/accounts/login', headers=headers_get)
    try:
        img = etree.HTML(response.text).xpath('//img[@id="captcha_image"]/@src')[0]
    except:
        img = ''
    print img

    try:
        captcha_id = etree.HTML(response.text).xpath('//div[@class="captcha_block"]/input[@name="captcha-id"]/@value')[0]
    except:
        captcha_id = ''
    print captcha_id

    req_timeout = 20

    try:
        if img:
            req = urllib2.Request(img, None, headers_get)
            page = urllib2.urlopen(req, None, req_timeout)

            content2 = page.read()
            with open(u'./tmp/' + img[-11:] + '.jpeg', 'wb') as code:
                code.write(content2)

    except urllib2.URLError as e:
            print e.message


    if img:
        code = verification_code_from_path(u'./tmp/' + img[-11:] + '.jpeg')
        print code

    session = requests.session()
    url = LOGIN_URL
    # 取第1个
    payload = {
        'redir': 'http://www.baidu.com',
        'source': None,
        'form_email': ACCOUNTS[1]['account'],
        'form_password': ACCOUNTS[1]['pass'],
        'captcha_field': '',
        'captcha-id': captcha_id
    }
    r = session.post(url, data=payload)
    print r.text
    # for k, v in r.cookies.items():
    #     print k, v
    ckies = requests.utils.dict_from_cookiejar(session.cookies)
    return ckies


if __name__ == '__main__':
    cookies = login()
    print cookies
    reply(cookies)
