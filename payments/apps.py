# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import (
    ProjectType, PluginURLs, PluginSettings, SettingsType
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
                SettingsType.DEVSTACK: {PluginSettings.RELATIVE_PATH: u'settings.lms_production'},
                SettingsType.AWS: {PluginSettings.RELATIVE_PATH: u'settings.lms_production'},
                SettingsType.PRODUCTION: {PluginSettings.RELATIVE_PATH: u'settings.lms_production'},
            }
        },
    }



