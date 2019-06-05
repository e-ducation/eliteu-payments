# -*- coding: utf-8 -*-
"""
Created on 2015-11-18
支付宝接口
@author: fengri
"""
from __future__ import unicode_literals

import types
import time
import logging

from urllib import urlencode, urlopen
from hashcompat import md5_constructor as md5

from config import ALIPAYSettings

log = logging.getLogger(__name__)

# 网关地址
_GATEWAY = 'https://mapi.alipay.com/gateway.do?'

SERVER_URL = 'https://openapi.alipay.com/gateway.do'


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
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, ALIPAYSettings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign', 'sign_type') and v != '':
            newparams[k] = smart_str(v, ALIPAYSettings.ALIPAY_INPUT_CHARSET)
            prestr += '%s=%s&' % (k, newparams[k])
    prestr = prestr[:-1]
    return newparams, prestr


# 生成签名结果
def build_mysign(prestr, key, sign_type='MD5'):
    if sign_type == 'MD5':
        return md5(prestr + key).hexdigest()
    return ''


# 即时到账交易接口
def create_direct_pay_by_user(tn, body, subject, total_fee, http_host, extra_common_param=''):
    log.info('------create direct pay by -user------------------')
    log.info(extra_common_param)
    log.info(body)
    params = {}
    params['service'] = 'create_direct_pay_by_user'
    params['payment_type'] = '1'

    # 获取配置文件
    params['partner'] = ALIPAYSettings.ALIPAY_PARTNER
    params['seller_id'] = ALIPAYSettings.ALIPAY_PARTNER
    params['seller_email'] = ALIPAYSettings.ALIPAY_SELLER_EMAIL

    return_url = ALIPAYSettings.ALIPAY_RETURN_URL
    split_items = return_url.split('/')
    new_items = [http_host if '.' in item else item for item in split_items]
    return_url = '/'.join(new_items)
    params['return_url'] = return_url

    notify_url = ALIPAYSettings.ALIPAY_NOTIFY_URL
    split_items = notify_url.split('/')
    new_items = [http_host if '.' in item else item for item in split_items]
    notify_url = '/'.join(new_items)
    params['notify_url'] = notify_url

    params['_input_charset'] = ALIPAYSettings.ALIPAY_INPUT_CHARSET
    params['show_url'] = ALIPAYSettings.ALIPAY_SHOW_URL

    # 从订单数据中动态获取到的必填参数
    params['out_trade_no'] = tn        # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject    # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = body       # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['total_fee'] = total_fee    # 订单总金额，显示在支付宝收银台里的“应付总额”里

    # 扩展功能参数——网银提前
    params['paymethod'] = 'directPay'   # 默认支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)
    params['defaultbank'] = ''          # 默认网银代号，代号列表见http://club.alipay.com/read.php?tid=8681379

    # 扩展功能参数——防钓鱼
    params['anti_phishing_key'] = ''
    params['exter_invoke_ip'] = ''

    # 扩展功能参数——自定义参数
    params['buyer_email'] = ''
    params['extra_common_param'] = extra_common_param

    # 扩展功能参数——分润
    params['royalty_type'] = ''
    params['royalty_parameters'] = ''

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, ALIPAYSettings.ALIPAY_KEY, ALIPAYSettings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = ALIPAYSettings.ALIPAY_SIGN_TYPE
    log.error(_GATEWAY + urlencode(params))
    return _GATEWAY + urlencode(params)


def create_direct_net_pay_by_user(tn, subject, body, total_fee, default_bank):
    """
    网银支付接口
    :param tn:
    :param subject:
    :param body:
    :param total_fee:
    :param default_bank:
    :return:
    """
    params = {}
    params['service'] = 'create_direct_pay_by_user'
    params['payment_type'] = '1'

    # 获取配置文件
    params['partner'] = ALIPAYSettings.ALIPAY_PARTNER
    params['_input_charset'] = ALIPAYSettings.ALIPAY_INPUT_CHARSET
    params['seller_id'] = ALIPAYSettings.ALIPAY_PARTNER
    params['seller_email'] = ALIPAYSettings.ALIPAY_SELLER_EMAIL
    params['return_url'] = ALIPAYSettings.ALIPAY_RETURN_URL
    params['notify_url'] = ALIPAYSettings.ALIPAY_NOTIFY_URL
    params['show_url'] = ALIPAYSettings.ALIPAY_SHOW_URL

    # 从订单数据中动态获取到的必填参数
    params['out_trade_no'] = tn        # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject   # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = body      # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['total_fee'] = total_fee    # 订单总金额，显示在支付宝收银台里的“应付总额”里

    # 扩展功能参数——网银提前
    params['paymethod'] = 'bankPay'    # 默认支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)
    params['defaultbank'] = default_bank          # 默认网银代号，代号列表见http://club.alipay.com/read.php?tid=8681379

    #扩展功能参数-网银支付时是否做CTU校验
    params['need_ctu_check'] = 'Y'

    # 扩展功能参数——防钓鱼
    params['anti_phishing_key'] = ''
    params['exter_invoke_ip'] = ''

    # 扩展功能参数——自定义参数
    params['extra_common_param'] = ''
    params['extend_param'] = ''

    #超时时间
    params['it_b_pay'] = ''

    #商户申请的产品类型
    params['product_type'] = ''

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, ALIPAYSettings.ALIPAY_KEY, ALIPAYSettings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = ALIPAYSettings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)


def create_partner_trade_by_buyer(tn, subject, body, price):
    """
    纯担保交易接口
    :param tn:
    :param subject:
    :param body:
    :param price:
    :return:
    """
    params = {}
    # 基本参数
    params['service'] = 'create_partner_trade_by_buyer'
    params['partner'] = ALIPAYSettings.ALIPAY_PARTNER
    params['_input_charset'] = ALIPAYSettings.ALIPAY_INPUT_CHARSET
    params['notify_url'] = ALIPAYSettings.ALIPAY_NOTIFY_URL
    params['return_url'] = ALIPAYSettings.ALIPAY_RETURN_URL

    # 业务参数
    params['out_trade_no'] = tn        # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject   # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['payment_type'] = '1'
    params['logistics_type'] = 'POST'   # 第一组物流类型
    params['logistics_fee'] = '0.00'
    params['logistics_payment'] = 'BUYER_PAY'
    params['price'] = price             # 订单总金额，显示在支付宝收银台里的“应付总额”里
    params['quantity'] = 1              # 商品的数量
    params['seller_email'] = ALIPAYSettings.ALIPAY_SELLER_EMAIL
    params['body'] = body      # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['show_url'] = ALIPAYSettings.ALIPAY_SHOW_URL

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, ALIPAYSettings.ALIPAY_KEY, ALIPAYSettings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = ALIPAYSettings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)


def create_refund_fastpay_by_user(batch_no, batch_num, detail_data):
    """
    refund_fastpay_by_platform_pwd
    service      接口名称       不可空      refund_fastpay_by_platform_pwd
    partner      合作者身份ID   不可空      2088101008267254
    _input_charset 参数编码字符集 不可空     GBK
    sign_type      签名方式      不可空     MD5
    sign           签名          不可空
    notify_url     服务器异步通知页面路径 可空
    业务参数
    seller_email    卖家支付宝账号 不可空
    seller_user_id  卖家用户ID  不可空 都填以user_id为准
    refund_date     退款请求时间 不可空 格式 yyyy-MM-dd hh:mm:ss
    batch_no       退款批次号    每进行一次即时到帐批量退款,都需要提供一个批次号,
    通过该批次号可以查询这一批次的退款交易记录,对于每一个合作伙伴,传递的每一个批次号都必须保证唯一性.
    格式为:退款日期(8位)+流水号(3-24位).不可重复,且退款日期必须是当天日期,流水号不能接受000,但可以是字母.
    例如:201101120001
    batch_num 总笔数 1-1000 不可空
    detail_data 单笔数据集  不可空 2011011201037066^500^协商退款

    https://mapi.alipay.com/gateway.do?seller_email=**&batch_num=1&refund_date=2011&notify_url=**&sign=**
    &service=refund_fastpay_by_platform_pwd&partner=**&detail_data=2****&sign_type=MD5&batch_no=20*
    :return:
    """
    params = {}
    # 基本参数
    params['service'] = 'refund_fastpay_by_platform_pwd'
    params['partner'] = ALIPAYSettings.ALIPAY_PARTNER
    params['_input_charset'] = ALIPAYSettings.ALIPAY_INPUT_CHARSET
    params['notify_url'] = ALIPAYSettings.ALIPAY_REFUND_NOTIFY_URL

    # 业务参数
    params['seller_email'] = ALIPAYSettings.ALIPAY_SELLER_EMAIL
    params['refund_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['batch_no'] = batch_no
    params['batch_num'] = batch_num
    params['detail_data'] = detail_data
    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, ALIPAYSettings.ALIPAY_KEY, ALIPAYSettings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = ALIPAYSettings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)


def send_goods_confirm_by_platform(tn):
    """
    确认发货接口
    :param tn:
    :return:
    """
    params = {}

    # 基本参数
    params['service'] = 'send_goods_confirm_by_platform'
    params['partner'] = ALIPAYSettings.ALIPAY_PARTNER
    params['_input_charset'] = ALIPAYSettings.ALIPAY_INPUT_CHARSET

    # 业务参数
    params['trade_no'] = tn
    params['logistics_name'] = u'英荔快递'   # 物流公司名称
    params['transport_type'] = u'POST'

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, ALIPAYSettings.ALIPAY_KEY, ALIPAYSettings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = ALIPAYSettings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)


def notify_verify(post):
    """
    初级验证--签名
    :param post:
    :return:
    """
    _, prestr = params_filter(post)
    mysign = build_mysign(prestr, ALIPAYSettings.ALIPAY_KEY, ALIPAYSettings.ALIPAY_SIGN_TYPE)
    if mysign != post.get('sign'):
        return False

    # 二级验证--查询支付宝服务器此条信息是否有效
    params = {}
    params['partner'] = ALIPAYSettings.ALIPAY_PARTNER
    params['notify_id'] = post.get('notify_id')
    if ALIPAYSettings.ALIPAY_TRANSPORT == 'https':
        params['service'] = 'notify_verify'
        gateway = 'https://mapi.alipay.com/gateway.do'
    else:
        gateway = 'http://notify.alipay.com/trade/notify_query.do'
    veryfy_result = urlopen(gateway, urlencode(params)).read()
    if veryfy_result.lower().strip() == 'true':
        return True
    return False


class AlipayVerify(object):
    """
    验签
    """

    def __init__(self):
        self.data = {}

    def saveData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def checkSign(self):
        return notify_verify(self.data)
