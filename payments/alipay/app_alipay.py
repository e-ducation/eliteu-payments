# -*- coding: utf-8 -*-

import rsa
import types
import base64
from django.conf import settings


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only, errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


class AlipayAppVerify(object):
    """
    验签
    """
    def __init__(self):
        self.data = {}
        with open(settings.ALIPAY_APP_INFO['basic_info']['ALIPAY_RSA_PUBLIC_KEY'], 'r') as fp:
            self.public_key = fp.read()

    def saveData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def checkSign(self):
        params = []
        sign = base64.b64decode(self.data['sign'])
        for k, v in sorted(self.data.items()):
            if k not in ('sign', 'sign_type'):
                params.append('{k}={v}'.format(k=smart_str(k), v=smart_str(v)))
        sign_params = '&'.join(params)
        return rsa.verify(sign_params, sign, rsa.PublicKey.load_pkcs1_openssl_pem(self.public_key))
