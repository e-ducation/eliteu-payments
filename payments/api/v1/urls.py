# -*- coding: utf-8 -*-
"""
URLs for payments api.
"""
from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    AlipaySuccessAPIView,
    AlipayAsyncnotifyAPIView,
    WechatAsyncnotifyAPIView
)


urlpatterns = [
    url(
        r'payments/alipay/alipaysuccess/$',
        AlipaySuccessAPIView.as_view(),
        name='alipay_success'
    ),
    url(
        r'payments/alipay/alipayasyncnotify/$',
        AlipayAsyncnotifyAPIView.as_view(),
        name='alipay_asyncnotify'
    ),
    url(
        r'payments/wechat/wechatasyncnotify/$',
        WechatAsyncnotifyAPIView.as_view(),
        name='wechat_asyncnotify'
    ),
]
