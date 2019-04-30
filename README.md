# eliteu payments

Introduction
------------
eliteu-payments是一个django app，我们把它当作一个支付回调的中转站。当你的网站接入多个第三方支付时，只需要一个支付的回调url，eliteu-payments会把支付类型及支付平台的返回信息全部传递给该url。


Installation
------------
```shell
pip install git+https://github.com/e-ducation/eliteu-payments
```

Usage
-----

### 设置回调url
- alipay
```python
from payments.alipay.alipay import create_direct_pay_by_user
create_direct_pay_by_user(trade_id, body, subject, total_fee, http_host,
                          extra_common_param=extra_common_param)
# extra_common_param为alipay的回调url
```
- alipay-app

    **设置passback_params参数值为回调url**

- wechatpay, wechatpay-app, wechatpay-h5

    **设置attach参数值为回调url**

### urls.py
```python
# 在你的项目的主urls.py下添加eliteu-payments的urls
urlpatterns += [
    url(r'', include('payments.urls')),
]
```

### settings.py

根据支付类型在settings.py配置支付基本信息

- alipay
```python
ALIPAY_INFO = {
    "basic_info":{
        "KEY": "",
        "PARTNER": "",
        "SELLER_EMAIL": ""
    },
    "other_info":{
        "INPUT_CHARSET": "",
        "INPUT_DIRECT_CHARSET": "",
        "SIGN_TYPE": "",
        "RETURN_URL": "",
        "NOTIFY_URL": "",
        "PAY_RESULT_URL": "",
        "REFUND_NOTIFY_URL": "",
        "SHOW_URL": "",
        "ERROR_NOTIFY_URL": "",
        "TRANSPORT": "",
        "DEFAULT_BANK": "",
        "IT_B_PAY": "",
        "REFUND_URL": ""
    }
}
```
- alipay-app
```python
ALIPAY_APP_INFO = {
    "basic_info":{
        "APP_ID": "",
        "APP_PRIVATE_KEY": "",
        "ALIPAY_RSA_PUBLIC_KEY": ""
    },
    "other_info":{
        "SIGN_TYPE": "",
        "NOTIFY_URL": ""
    }
}
```

- wechatpay
```python
WECHAT_PAY_INFO = {
    "basic_info":{
        "APPID": "",
        "APPSECRET": "",
        "MCHID": "",
        "KEY": "",
        "ACCESS_TOKEN": ""
    },
    "other_info":{
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
```
- wechatpay-app
```python
WECHAT_APP_PAY_INFO = {
    "basic_info":{
        "APPID": "",
        "APPSECRET": "",
        "MCHID": "",
        "KEY": "",
        "ACCESS_TOKEN": ""
    },
    "other_info":{
        "NOTIFY_URL": ""
    }
}
```
- wechatpay-h5
```python
WECHAT_H5_PAY_INFO = {
    "basic_info":{
        "APPID": "",
        "APPSECRET": "",
        "MCHID": "",
        "KEY": "",
        "ACCESS_TOKEN": ""
    },
    "other_info":{
        "SERVICE_TEL": "",
        "NOTIFY_URL": "",
        "JS_API_CALL_URL": "",
        "SSLCERT_PATH": "",
        "SSLKEY_PATH": "",
        "SPBILL_CREATE_IP": ""
    }
}
```


License
-------

The code in this repository is licensed under AGPL unless otherwise noted.

Please see LICENSE for details.

How To Contribute
-----------------

Contributions are very welcome.

Please read [How To Contribute](https://github.com/e-ducation/eliteu-payments/blob/master/CONTRIBUTING.md) for details.
