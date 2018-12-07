# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import thread
import logging
import requests

from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse

from rest_framework.views import APIView

from payments.alipay.alipay import notify_verify as alipay_notify_verify
from payments.alipay.app_alipay import notify_verify as app_alipay_notify_verify
from payments.wechatpay.wxpay import Wxpay_server_pub
from payments.alipay.config import ALIPAYSettings
# 需要放在安全区的变量
dish = 0
lock = thread.allocate_lock()
log = logging.getLogger(__name__)


class AlipaySuccessAPIView(APIView):
    """
    alipay success api view
    """

    def get(self, request, *args, **kwargs):
        """
        create order
        ---
        支付宝支付 同步
        GET传递参数 同步
            1.用户在登录成功后会看到一个支付宝提示登录的页面，该页面会停留几秒，然后会自动跳转回商户指定的同步通知页面（参数return_url）。
            2.该页面中获得参数的方式，需要使用GET方式获取，如request.QueryString(“out_trade_no”)、$_GET[‘out_trade_no’]。后续商户可根据获取的信息作处理，譬如，可以把获取到的token放入session中，以便于后续需要使用到token访问支付宝相应服务时，可以便捷地重用。
            3.该方式仅仅在用户登录完成以后进行自动跳转，因此只会进行一次。
            4.该方式不是支付宝主动去调用商户页面，而是支付宝的程序利用页面自动跳转的函数，使用户的当前页面自动跳转。
            5.该方式可在本机而不是只能在服务器上进行调试。
            6.返回URL只有一分钟的有效期，超过一分钟该链接地址会失效，验证则会失败。
            7.设置页面跳转同步通知页面（return_url）的路径时，不要在页面文件的后面再加上自定义参数。
            8.由于支付宝会对页面跳转同步通知页面（return_url）的域名进行合法有效性校验，因此设置页面跳转同步通知页面（return_url）的路径时，不要设置成本机域名，也不能带有特殊字符（如“!”），如：买家付款成功后，如果接口中指定有return_url,买家付完款后会调到return_url所在的页面。 这个页面可以展示给客户看。这个页面只有付款成功后才会跳转。
        """

        global lock, dish
        if alipay_notify_verify(request.query_params):
            out_trade_no = request.query_params.get("out_trade_no", "")
            extra_common_param = request.query_params.get("extra_common_param")

            post_data = {
                "trade_type": "alipay",
                "out_trade_no": out_trade_no,
                "extra_common_param": extra_common_param,
                "trade_no": request.query_params.get("trade_no"),
                "total_fee": request.query_params.get("total_fee"),
                "trade_email": request.query_params.get("buyer_email"),
            }
            url_str = ALIPAYSettings.PAY_RESULT_URL + "?out_trade_no=" + out_trade_no
            if out_trade_no != "":
                rep = requests.post(extra_common_param, data=post_data)
                rep_data = rep.json()
                if rep_data.get('result') == "success":
                    return HttpResponseRedirect(url_str)
                return HttpResponseRedirect(url_str)
            else:
                return HttpResponseRedirect(url_str)
        else:
            return HttpResponse("fail")


class AlipayAsyncnotifyAPIView(APIView):
    """
    alipay asyncnotify api view
    """

    def post(self, request, *args, **kwargs):
        """
        支付宝支付 异步
        服务器后台通知，买家付完款后，支付宝会调用notify_url这个页面所在的页面，并把相应的参数传递到这个页面，
        这个页面根据支付宝传递过来的参数修改网站订单的状态。
        更新完订单后需要在页面上打印一个success给支付宝，如果反馈给支付宝的不是success,支付宝会继续调用这个页面。
        传递过来的参数是post格式
        商户需要验证该通知数据中的out_trade_no是否为商户系统中创建的订单号，
        并判断total_fee是否确实为该订单的实际金额（即商户订单创建时的金额），
        同时需要校验通知中的seller_id（或者seller_email) 是否为out_trade_no这笔单据的对应的操作方，
        （有的时候，一个商户可能有多个seller_id/seller_email），
        上述有任何一个验证不通过，则表明本次通知是异常通知，务必忽略。
        在上述验证通过后商户必须根据支付宝不同类型的业务通知，正确的进行不同的业务处理，并且过滤重复的通知结果数据。
        在支付宝的业务通知中，只有交易通知状态为TRADE_SUCCESS或TRADE_FINISHED时，支付宝才会认定为买家付款成功。
        如果商户需要对同步返回的数据做验签，必须通过服务端的签名验签代码逻辑来实现。
        如果商户未正确处理业务通知，存在潜在的风险，商户自行承担因此而产生的所有损失。
        """

        global lock, dish
        if alipay_notify_verify(request.data):
            extra_common_param = request.data.get("extra_common_param")
            out_trade_no = request.data.get("out_trade_no", "")

            post_data = {
                "trade_type": "alipay",
                "out_trade_no": out_trade_no,
                "trade_no": request.data.get("trade_no"),
                "total_fee": request.data.get("total_fee"),
                "buyer_email": request.data.get("buyer_email"),
                "extra_common_param": request.data.get("extra_common_param"),
            }

            if out_trade_no != "":
                rep = requests.post(extra_common_param, data=post_data)
                rep_data = rep.json()
                if rep_data.get('result') == "success":
                    return HttpResponse('success')
        return HttpResponse("fail")


class AppAlipayAsyncnotifyAPIView(APIView):
    """
    alipay asyncnotify api view
    """

    def post(self, request, *args, **kwargs):
        """
        支付宝支付 异步
        服务器后台通知，买家付完款后，支付宝会调用notify_url这个页面所在的页面，并把相应的参数传递到这个页面，
        这个页面根据支付宝传递过来的参数修改网站订单的状态。
        更新完订单后需要在页面上打印一个success给支付宝，如果反馈给支付宝的不是success,支付宝会继续调用这个页面。
        传递过来的参数是post格式
        商户需要验证该通知数据中的out_trade_no是否为商户系统中创建的订单号，
        并判断total_fee是否确实为该订单的实际金额（即商户订单创建时的金额），
        同时需要校验通知中的seller_id（或者seller_email) 是否为out_trade_no这笔单据的对应的操作方，
        （有的时候，一个商户可能有多个seller_id/seller_email），
        上述有任何一个验证不通过，则表明本次通知是异常通知，务必忽略。
        在上述验证通过后商户必须根据支付宝不同类型的业务通知，正确的进行不同的业务处理，并且过滤重复的通知结果数据。
        在支付宝的业务通知中，只有交易通知状态为TRADE_SUCCESS或TRADE_FINISHED时，支付宝才会认定为买家付款成功。
        如果商户需要对同步返回的数据做验签，必须通过服务端的签名验签代码逻辑来实现。
        如果商户未正确处理业务通知，存在潜在的风险，商户自行承担因此而产生的所有损失。
        """

        global lock, dish
        if app_alipay_notify_verify(request.data):
            extra_common_param = request.data.get("extra_common_param")
            out_trade_no = request.data.get("out_trade_no", "")

            post_data = {
                "trade_type": "alipay",
                "out_trade_no": out_trade_no,
                "trade_no": request.data.get("trade_no"),
                "total_fee": request.data.get("total_fee"),
                "buyer_email": request.data.get("buyer_email"),
                "extra_common_param": request.data.get("extra_common_param"),
            }

            if out_trade_no != "":
                rep = requests.post(extra_common_param, data=post_data)
                rep_data = rep.json()
                if rep_data.get('result') == "success":
                    return HttpResponse('success')
        return HttpResponse("fail")


class WechatAsyncnotifyAPIView(APIView):
    """
    wechat asyncnotify api view
    """

    def post(self, request, *args, **kwargs):
        """
        微信回调支付
        """
        wxpay_server_pub = Wxpay_server_pub()
        wxpay_server_pub.saveData(request.body)
        ret_str = 'FAIL'
        if wxpay_server_pub.checkSign():
            pay_result = wxpay_server_pub.getData()
            post_data = {
                'trade_type': 'wechat',
                'trade_no': pay_result.get('transaction_id'),
                'out_trade_no': pay_result.get('out_trade_no'),
            }
            if pay_result.get('attach'):
                rep = requests.post(pay_result['attach'], data=post_data)
                rep_data = rep.json()
                if rep_data.get('result') == "success":
                    ret_str = 'SUCCESS'
        return HttpResponse(wxpay_server_pub.arrayToXml({'return_code': ret_str}))
