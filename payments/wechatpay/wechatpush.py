# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import json
import urllib2


class WechatPush(object):

    def __init__(self, appid, secrect):
        self.appid = appid
        self.secrect = secrect

    # 获取accessToken
    def getToken(self):
        # 判断缓存
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + self.appid + "&secret=" + self.secrect
        f = urllib2.urlopen(url)
        s = f.read()
        # 读取json数据
        j = json.loads(s)
        j.keys()
        token = j['access_token']
        return token

    # 获取基本信息
    def get_user_info(self, access_token, openid, lang='zh_CN'):
        """
        获取用户基本信息
        详情请参考
        http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
        http请求方式: GET
        https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        """

        assert lang in ('zh_CN', 'zh_TW', 'en'), 'lang can only be one of \
            zh_CN, zh_TW, en language codes'

        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=' + access_token + '&openid=' + openid + "&lang=" + lang
        f = urllib2.urlopen(url)
        s = f.read()
        # 读取json数据
        j = json.loads(s)
        # j.keys()

        return j

    # 开始推送
    def do_push(self, touser, template_id, url, data, topcolor):
        if topcolor.strip() == '':
            topcolor = "#7B68EE"
        dict_arr = {'touser': touser, 'template_id': template_id, 'url': url, 'topcolor': topcolor, 'data': data}
        json_template = json.dumps(dict_arr)
        token = self.getToken()
        requst_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + token
        content = self.post_data(requst_url, json_template)
        # 读取json数据
        j = json.loads(content)
        j.keys()
        errcode = j['errcode']
        errmsg = j['errmsg']
        return errmsg

    # 模拟post请求
    def post_data(self, url, para_dct):
        para_data = para_dct
        f = urllib2.urlopen(url, para_data)
        content = f.read()
        return content
