# -*- coding: utf-8 -*-
"""
URLs for payments api.
"""
from __future__ import unicode_literals

from django.conf.urls import url, include

urlpatterns = [
    url(r'v1/', include('payments.api.v1.urls'))
]
