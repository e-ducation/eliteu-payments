# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import (
    ProjectType, PluginURLs, PluginSettings
)


class PaymentsConfig(AppConfig):
    name = 'payments'
    verbose_name = 'Payments'

    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: u'payments',
                PluginURLs.REGEX: u'',
            }
        },
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                'devstack': {
                    PluginSettings.RELATIVE_PATH: u'settings.lms_production',
                },
            }
        },
    }



