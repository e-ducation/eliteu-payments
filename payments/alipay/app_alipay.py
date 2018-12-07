# -*- coding: utf-8 -*-
"""
Created on 2015-11-18
支付宝接口
@author: fengri
"""
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
import types
import time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
import base64
from base64 import b64decode
from urllib import urlencode, urlopen, unquote
from hashcompat import md5_constructor as md5
from Crypto.Signature import PKCS1_v1_5 as pk
from config import ALIPAYAPPSettings
import rsa
import requests
log = logging.getLogger(__name__)
"""
publickey为对方的公钥
privatekey为商户自己的私钥
"""
PRIVATE_KEY = RSA.importKey(open('/edx/app/edxapp/ali_pay/certs/app_private_key_pkcs8.pem', 'r').read())

# 支付宝 RSA 公钥
ALIPAY_RSA_PUBLIC_KEY_PATH = '/edx/app/edxapp/ali_pay/certs/app_public_key.pem'

# 验证是否是支付宝发来的通知链接地址
ALIPAY_REMOTE_ORIGIN_URL = 'https://mapi.alipay.com/gateway.do'

# 网关地址
_GATEWAY = 'https://mapi.alipay.com/gateway.do?'


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only, errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


def params_filter(params):
    """
    # 对数组排序并除去数组中的空值和签名参数
    # 返回数组和链接串
    :param params:
    :return:
    """
    ks = params.keys()
    ks.sort()
    new_params = {}
    pre_str = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, ALIPAYAPPSettings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign', 'sign_type') and v != '':
            new_params[k] = smart_str(v, ALIPAYAPPSettings.ALIPAY_INPUT_CHARSET)
            pre_str += '%s=%s&' % (k, new_params[k])
    pre_str = pre_str[:-1]
    return new_params, pre_str


def params_join(params):
    """
    # 对数组排序并除去数组中的空值和签名参数
    # 返回数组和链接串
    :param params:
    :return:
    """
    ks = params.keys()
    ks.sort()
    new_params = {}
    pre_str = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, ALIPAYAPPSettings.ALIPAY_INPUT_CHARSET)
        new_params[k] = smart_str(v, ALIPAYAPPSettings.ALIPAY_INPUT_CHARSET)
        pre_str += '%s=\"%s\"&' % (k, new_params[k])
    pre_str = pre_str[:-1]
    return new_params, pre_str

'''
RSA签名
'''


def sign(sign_data):
    """
    @param sign_data: 需要签名的字符串
    """
    signer = pk.new(PRIVATE_KEY)
    digest = SHA.new()
    digest.update(sign_data)
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    return signature


'''
RSA验签
结果：如果验签通过，则返回The signature is authentic
     如果验签不通过，则返回"The signature is not authentic."
    '''


def check_sign(rdata):
    """
    验证签名
    :param rdata:
    :return:
    https://mapi.alipay.com/gateway.do?service=notify_verify&partner=2088002396712354
        &notify_id=RqPnCoPT3K9%252Fvwbh3I%252BFioE227%252BPfNMl8jwyZqMIiXQWxhOCmQ5MQO%252FWd93rvCB%252BaiGg
    """

    signn = rdata.get('sign')
    new_params, msg = params_filter(rdata)
    key = RSA.importKey(open('/edx/app/edxapp/edx-platform/common/djangoapps/ali_pay/certs/app_public_key.pem').read())
    signn = b64decode(signn)
    h = SHA.new(msg)
    verifier = pk.new(key)
    if verifier.verify(h, signn):
        params = urlencode({'service': rdata.get('service'), 'partner': rdata.get('partner'), 'notify_id': rdata.get('notify_id')})
        is_alipay_notify = urlopen("https://mapi.alipay.com/gateway.do?%s" % params)
        if is_alipay_notify:
            return True
        else:
            return False
    else:
        return False


# 验证签名
# params：request.POST
def verifySignString(params):
    if not len(params) > 0:
        return False
    key_sorted = sorted(params.keys())
    content = ''
    sign_type = params["sign_type"]
    signOrigin = params["sign"]

    for key in key_sorted:
        if key not in ["sign", "sign_type"]:
            if len(params[key]) > 0:
                content = content + key + "=" + params[key] + "&"
    content = content[:-1]
    content = content.encode("utf-8")
    # print "content -> " + content

    if sign_type.upper() == "RSA":
        try:
            with open('/edx/app/edxapp/edx-platform/common/djangoapps/ali_pay/certs/alipay_public_key.pem') as publickfile:
                pub = publickfile.read()
            pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(pub)

            # 支付宝返回的 sign 经过 base64 encode，先 decode 一下
            signatureString = base64.decodestring(signOrigin)
            if rsa.verify(content, signatureString, pubkey):
                # print "----------verify sign success----------"
                return True
        except Exception as ex:
            # print "----------verify sign failed----------"
            return False
    else:
        # 支付宝当前仅支持 RSA 加密，未来也许会有其他类型
        return False

    return False


def verifyURL(partner, notify_id):
    """
    # 验证是否是支付宝发来的通知
    # partner：request.POST["seller_id"]，也可以 hardcode
    # notify_id：request.POST["notify_id"]
    :param partner:
    :param notify_id:
    :return:
    """
    payload = {'service': 'notify_verify', 'partner': partner, 'notify_id': notify_id}
    urlString = ALIPAY_REMOTE_ORIGIN_URL
    r = requests.get(urlString, params=payload)
    result = r.text
    # print result
    if result.upper() == "TRUE":
        # print "----------verify url success----------"
        return True
    return False


def sort(params):
    """
    作用类似与java的treemap,
    取出key值,按照字母排序后将value拼接起来
    返回字符串
    """
    ks = params.keys()
    ks.sort()
    pre_str = ''
    for k in ks:
        v = params[k]
        if k not in ('sign', 'sign_type') and v != '':
            pre_str += '%s=%s&' % (k, unquote(params[k]))
    pre_str = pre_str[:-1]
    return pre_str


def notify_verify(post):
    """
    初级验证--签名
    :param post:
    :return:
    """
    _, prestr = params_filter(post)
    mysign = sign(prestr)
    if mysign != post.get('sign'):
        return False

    # 二级验证--查询支付宝服务器此条信息是否有效
    params = {}
    params['partner'] = ALIPAYAPPSettings.ALIPAY_PARTNER
    params['notify_id'] = post.get('notify_id')
    if ALIPAYAPPSettings.ALIPAY_TRANSPORT == 'https':
        params['service'] = 'notify_verify'
        gateway = 'https://mapi.alipay.com/gateway.do'
    else:
        gateway = 'http://notify.alipay.com/trade/notify_query.do'
    veryfy_result = urlopen(gateway, urlencode(params)).read()
    if veryfy_result.lower().strip() == 'true':
        return True
    return False


# APP支付接口
def create_app_pay_by_user(tn, subject, body, total_fee, extra_common_param=""):
    params = {}
    params['partner'] = "{partner}".format(partner=ALIPAYAPPSettings.ALIPAY_PARTNER)
    params['seller_id'] = "{seller_id}".format(seller_id=ALIPAYAPPSettings.ALIPAY_SELLER_EMAIL)
    params['out_trade_no'] = "{out_trade_no}".format(out_trade_no=unicode(tn))        # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = "{subject}".format(subject=subject)    # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = "{body}".format(body=body)
    params['total_fee'] = "{total_fee}".format(total_fee=total_fee)    # 订单总金额，显示在支付宝收银台里的“应付总额”里
    params['notify_url'] = "{notify_url}".format(notify_url=ALIPAYAPPSettings.ALIPAY_NOTIFY_URL)

    params['service'] = "mobile.securitypay.pay"
    params['payment_type'] = "1"
    params['_input_charset'] = "{input_charset}".format(input_charset=ALIPAYAPPSettings.ALIPAY_INPUT_CHARSET)
    params['it_b_pay'] = "30m"
    params['return_url'] = ""
    params['extra_common_param'] = extra_common_param

    prestr = 'partner=\"{partner}\"&seller_id=\"{seller_id}\"&out_trade_no=\"{out_trade_no}\"&subject=\"{subject}\"&body=\"{body}\"' \
             '' \
             '&total_fee=\"{total_fee}\"&notify_url=\"{notify_url}\"&service=\"{service}\"&payment_type=\"{payment_type}\"' \
             '&_input_charset=\"{input_charset}\"&extra_common_param=\"{extra_common_param}\"'.format(partner=params['partner'], seller_id=params['seller_id'], out_trade_no=params['out_trade_no'],
                                                          subject=params['subject'], body=params['body'], total_fee=params['total_fee'], notify_url=params['notify_url'],
                                                          service=params['service'], payment_type=params['payment_type'], input_charset=params['_input_charset'],
                                                          extra_common_param=params['extra_common_param'])
    params['sign'] = sign(prestr)
    params['sign_type'] = "{sign_type}".format(sign_type=ALIPAYAPPSettings.ALIPAY_SIGN_TYPE)
    return params
