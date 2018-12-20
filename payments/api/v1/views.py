# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import json
import thread
import logging
import requests

from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView
from payments.alipay.alipay import notify_verify
from payments.alipay.app_alipay import AlipayAppVerify
from payments.wechatpay.wxapp_pay import Wxpay_server_pub as AppWxpay_server_pub
from payments.wechatpay.wxpay import Wxpay_server_pub
from payments.wechatpay.wxh5_pay import WxpayH5_server_pub
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
        log.info('************ alipay query params ************')
        if notify_verify(request.query_params):
            out_trade_no = request.query_params.get("out_trade_no", "")
            extra_common_param = request.query_params.get("extra_common_param")

            post_data = {
                "trade_type": "alipay",
                'out_trade_no': out_trade_no,
                "total_fee": request.query_params.get("total_fee"),
                "original_data": json.dumps({'data': request.query_params}),
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

        try:
            log.info('************ alipay notify data ************')
            log.info(request.data)
            if notify_verify(request.data):
                extra_common_param = request.data.get("extra_common_param")
                out_trade_no = request.data.get("out_trade_no", "")

                post_data = {
                    "trade_type": "alipay",
                    'out_trade_no': out_trade_no,
                    "total_fee": request.data.get("total_fee"),
                    "original_data": json.dumps({'data': request.data}),
                }
                if out_trade_no != "":
                    rep = requests.post(extra_common_param, data=post_data)
                    rep_data = rep.json()
                    if rep_data.get('result') == "success":
                        return HttpResponse('success')
        except Exception, e:
            log.exception(e)
        return HttpResponse("fail")


class AppAlipayAsyncnotifyAPIView(APIView):

    def post(self, request, *args, **kwargs):
        """
        app alipay asyncnotify api view
        """
        try:
            log.info('************ alipay app notify data ************')
            log.info(request.data)
            verify_srv = AlipayAppVerify()
            verify_srv.saveData(request.data)
            if verify_srv.checkSign():
                passback_params = request.data.get("passback_params")
                out_trade_no = request.data.get("out_trade_no", "")
                post_data = {
                    "trade_type": "alipay_app",
                    "original_data": json.dumps({'data': request.data}),
                }
                if out_trade_no != "":
                    rep = requests.post(passback_params, data=post_data)
                    rep_data = rep.json()
                    if rep_data.get('result') == "success":
                        return HttpResponse('success')
        except Exception, e:
            log.exception(e)
        return HttpResponse("fail")


class WechatAsyncnotifyAPIView(APIView):
    """
    wechat asyncnotify api view
    """

    def post(self, request, *args, **kwargs):
        """
        微信回调支付
        """
        try:
            ret_str = 'FAIL'
            log.info('********** wechatpay notify **********')
            log.info(request.body)
            wxpay_server_pub = Wxpay_server_pub()  # NATIVE pay
            wxpay_server_pub.saveData(request.body)
            resp_trade_type = wxpay_server_pub.getData().get('trade_type')
            if resp_trade_type == "APP":
                wxpay_server_pub = AppWxpay_server_pub()
                wxpay_server_pub.saveData(request.body)
                trade_type = 'wechat_app'
            elif resp_trade_type == "NATIVE":
                trade_type = 'wechat'

            if wxpay_server_pub.checkSign():
                pay_result = wxpay_server_pub.getData()
                post_data = {
                    'trade_type': trade_type,
                    'out_trade_no': pay_result.get('out_trade_no'),
                    "total_fee": pay_result.get("total_fee"),
                    "original_data": json.dumps({'data': request.body}),
                }
                if pay_result.get('attach'):
                    rep = requests.post(pay_result['attach'], data=post_data)
                    rep_data = rep.json()
                    if rep_data.get('result') == "success":
                        ret_str = 'SUCCESS'
        except Exception, e:
            log.exception(e)
        return HttpResponse(wxpay_server_pub.arrayToXml({'return_code': ret_str}))


class WechatH5AsyncnotifyAPIView(APIView):
    """
    wechat H5 asyncnotify api view
    """

    def post(self, request, *args, **kwargs):
        """
        微信H5回调支付
        """
        wxpayh5_server_pub = WxpayH5_server_pub()
        wxpayh5_server_pub.saveData(request.body)
        log.error(request.body)
        ret_str = 'FAIL'

        if wxpayh5_server_pub.checkSign():
            pay_result = wxpayh5_server_pub.getData()
            post_data = {
                'trade_type': 'wechat_h5',
                'trade_no': pay_result.get('transaction_id'),
                "total_fee": pay_result.get("total_fee"),
                'out_trade_no': pay_result.get('out_trade_no'),
                "original_data": json.dumps({'data': request.body}),
            }
            if pay_result.get('attach'):
                rep = requests.post(pay_result['attach'], data=post_data)
                rep_data = rep.json()
                if rep_data.get('result') == "success":
                    ret_str = 'SUCCESS'
        return HttpResponse(wxpayh5_server_pub.arrayToXml({'return_code': ret_str}))
