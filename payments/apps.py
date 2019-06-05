# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import (
    ProjectType, SettingsType, PluginURLs, PluginSettings
)


def production_settings_name():
    """
    Helper for Hawthorn and Ironwood+ compatibility.

    This helper will explicitly break if something have changed in `SettingsType`.
    """
    if hasattr(SettingsType, 'AWS'):
        # Hawthorn and Ironwood
        return getattr(SettingsType, 'AWS')
    else:
        # Juniper and beyond.
        return getattr(SettingsType, 'PRODUCTION')


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

        # PluginSettings.CONFIG: {
        #     ProjectType.LMS: {
        #         production_settings_name(): {
        #             PluginSettings.RELATIVE_PATH: u'settings.lms_production',
        #         },
        #     }
        # },
    }



