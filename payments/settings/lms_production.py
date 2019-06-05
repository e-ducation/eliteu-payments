
# WECHAT_APP_PAY
WECHAT_APP_PAY_INFO = {
    "basic_info": {
        "APPID": "",
        "APPSECRET": "",
        "MCHID": "",
        "KEY": "",
        "ACCESS_TOKEN": ""
    },
    "other_info": {
        "BUY_COURSES_SUCCESS_TEMPLATE_ID": "",
        "BUY_COURSES_SUCCESS_HREF_URL": "",
        "COIN_SUCCESS_TEMPLATE_ID": "",
        "COIN_SUCCESS_HREF_URL": "",
        "SERVICE_TEL": "",
        "NOTIFY_URL": "",
        "JS_API_CALL_URL": "",
        "SSLCERT_PATH": "",
        "SSLKEY_PATH": ""
    }
}

# WECHAT_PAY
WECHAT_PAY_INFO = {
    "basic_info": {
        "APPID": "",
        "APPSECRET": "",
        "MCHID": "",
        "KEY": "",
        "ACCESS_TOKEN": ""
    },
    "other_info": {
        "BUY_COURSES_SUCCESS_TEMPLATE_ID": "",
        "BUY_COURSES_SUCCESS_HREF_URL": "",
        "COIN_SUCCESS_TEMPLATE_ID": "",
        "COIN_SUCCESS_HREF_URL": "",
        "SERVICE_TEL": "",
        "NOTIFY_URL": "",
        "JS_API_CALL_URL": "",
        "SSLCERT_PATH": "",
        "SSLKEY_PATH": ""
    }
}

# WECHAT H5 PAY
WECHAT_H5_PAY_INFO = {
    "basic_info": {
        "APPID": "",
        "APPSECRET": "",
        "MCHID": "",
        "KEY": "",
        "ACCESS_TOKEN": ""
    },
    "other_info": {
        "SERVICE_TEL": "",
        "NOTIFY_URL": "",
        "JS_API_CALL_URL": "",
        "SSLCERT_PATH": "",
        "SSLKEY_PATH": "",
        "SPBILL_CREATE_IP": ""
    }
}

# ALIPAY_INFO
ALIPAY_APP_INFO = {
    "basic_info": {
        "APP_ID": "",
        "APP_PRIVATE_KEY": "",
        "ALIPAY_RSA_PUBLIC_KEY": ""
    },
    "other_info": {
        "SIGN_TYPE": "",
        "NOTIFY_URL": ""
    }
}

# ALIPAY_INFO
ALIPAY_INFO = {
    'basic_info': {
        "KEY": "",
        "PARTNER": "",
        "SELLER_EMAIL": ""
    },
    'other_info': {
        "INPUT_CHARSET": "",
        "INPUT_DIRECT_CHARSET": "",
        "SIGN_TYPE": "",
        "RETURN_URL": "",
        "NOTIFY_URL": "",
        "REFUND_NOTIFY_URL": "",
        "SHOW_URL": "",
        "ERROR_NOTIFY_URL": "",
        "TRANSPORT": "",
        "DEFAULT_BANK": "",
        "IT_B_PAY": "",
        "REFUND_URL": ""
    }
}


def plugin_settings(settings):
    settings.ALIPAY_INFO = settings.AUTH_TOKENS.get('ALIPAY_INFO', ALIPAY_INFO)
    settings.ALIPAY_APP_INFO = settings.AUTH_TOKENS.get('ALIPAY_APP_INFO', ALIPAY_APP_INFO)
    settings.WECHAT_PAY_INFO = settings.AUTH_TOKENS.get('WECHAT_PAY_INFO', WECHAT_PAY_INFO)
    settings.WECHAT_APP_PAY_INFO = settings.AUTH_TOKENS.get('WECHAT_APP_PAY_INFO', WECHAT_APP_PAY_INFO)
    settings.WECHAT_H5_PAY_INFO = settings.AUTH_TOKENS.get('WECHAT_H5_PAY_INFO', WECHAT_H5_PAY_INFO)