# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


class ALIPAYSettings:
    # 安全检验码，以数字和字母组成的32位字符
    ALIPAY_KEY = settings.ALIPAY_INFO['basic_info']['KEY']

    # 合作身份者ID，以2088开头的16位纯数字
    ALIPAY_PARTNER = settings.ALIPAY_INFO['basic_info']['PARTNER']

    # 签约支付宝账号或卖家支付宝帐户
    ALIPAY_SELLER_EMAIL = settings.ALIPAY_INFO['basic_info']['SELLER_EMAIL']

    ALIPAY_INPUT_CHARSET = settings.ALIPAY_INFO['other_info']['INPUT_CHARSET']

    ALIPAY_INPUT_DIRECT_CHARSET = settings.ALIPAY_INFO['other_info']['INPUT_DIRECT_CHARSET']

    ALIPAY_SIGN_TYPE = settings.ALIPAY_INFO['other_info']['SIGN_TYPE']

    # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_RETURN_URL = settings.ALIPAY_INFO['other_info']['RETURN_URL']

    # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_NOTIFY_URL = settings.ALIPAY_INFO['other_info']['NOTIFY_URL']

    # 申请退款异步通知的页面
    ALIPAY_REFUND_NOTIFY_URL = settings.ALIPAY_INFO['other_info']['REFUND_NOTIFY_URL']

    ALIPAY_SHOW_URL = settings.ALIPAY_INFO['other_info']['SHOW_URL']

    # 请求时出错的通知地址可以是请求参数中提交的error_notify_url，也可以是支付宝为商户配置好的商户指定通知地址。
    # 如果两者都有设置，则以error_notify_url为准。
    ERROR_NOTIFY_URL = settings.ALIPAY_INFO['other_info']['ERROR_NOTIFY_URL']

    # 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
    ALIPAY_TRANSPORT = settings.ALIPAY_INFO['other_info']['TRANSPORT']

    # 默认网上银行
    DEFAULT_BANK = settings.ALIPAY_INFO['other_info']['DEFAULT_BANK']

    # 超时时间 设置未付款交易的超时时间，一旦超时，该笔交易就会自动被关闭 取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天（无论交易何时创建，都在0点关闭）。该参数数值不接受小数点，如1.5h，可转换为90m。
    IT_B_PAY = settings.ALIPAY_INFO['other_info']['IT_B_PAY']

    # 调用的接口名，无需修改
    REFUND_URL = settings.ALIPAY_INFO['other_info']['REFUND_URL']

    # 同步成功后返回的结果页面
    PAY_RESULT_URL = settings.ALIPAY_INFO['other_info']['PAY_RESULT_URL']


class ALIPAYAPPSettings:
    # 安全检验码，以数字和字母组成的32位字符
    ALIPAY_KEY = settings.ALIPAY_APP_INFO['basic_info']['KEY']

    # 合作身份者ID，以2088开头的16位纯数字
    ALIPAY_PARTNER = settings.ALIPAY_APP_INFO['basic_info']['PARTNER']

    # 签约支付宝账号或卖家支付宝帐户
    ALIPAY_SELLER_EMAIL = settings.ALIPAY_APP_INFO['basic_info']['SELLER_EMAIL']

    ALIPAY_INPUT_CHARSET = settings.ALIPAY_APP_INFO['other_info']['INPUT_CHARSET']

    ALIPAY_INPUT_DIRECT_CHARSET = settings.ALIPAY_APP_INFO['other_info']['INPUT_DIRECT_CHARSET']

    ALIPAY_SIGN_TYPE = settings.ALIPAY_APP_INFO['other_info']['SIGN_TYPE']

    # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_RETURN_URL = settings.ALIPAY_APP_INFO['other_info']['RETURN_URL']

    # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_NOTIFY_URL = settings.ALIPAY_APP_INFO['other_info']['NOTIFY_URL']

    # 申请退款异步通知的页面
    ALIPAY_REFUND_NOTIFY_URL = settings.ALIPAY_APP_INFO['other_info']['REFUND_NOTIFY_URL']

    ALIPAY_SHOW_URL = settings.ALIPAY_APP_INFO['other_info']['SHOW_URL']

    #请求时出错的通知地址可以是请求参数中提交的error_notify_url，也可以是支付宝为商户配置好的商户指定通知地址。如果两者都有设置，则以error_notify_url为准。
    ERROR_NOTIFY_URL = settings.ALIPAY_APP_INFO['other_info']['ERROR_NOTIFY_URL']

    # 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
    ALIPAY_TRANSPORT = settings.ALIPAY_APP_INFO['other_info']['TRANSPORT']

    #默认网上银行
    DEFAULT_BANK = settings.ALIPAY_APP_INFO['other_info']['DEFAULT_BANK']

    #超时时间 设置未付款交易的超时时间，一旦超时，该笔交易就会自动被关闭 取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天（无论交易何时创建，都在0点关闭）。该参数数值不接受小数点，如1.5h，可转换为90m。
    IT_B_PAY = settings.ALIPAY_APP_INFO['other_info']['IT_B_PAY']

    #调用的接口名，无需修改
    REFUND_URL = settings.ALIPAY_APP_INFO['other_info']['REFUND_URL']