# -*- coding: utf-8 -*-
"""
URLs for payments.
"""
from __future__ import unicode_literals

from django.conf.urls import url, include


urlpatterns = [
    url(r'^api/', include('payments.api.urls'))
]
