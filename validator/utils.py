# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six

def force_text(s, encoding='utf8', errors='strict'):
    if isinstance(s, six.text_type):
        return s
    if not issubclass(type(s), six.string_types):
        if six.PY3:
            if isinstance(s, bytes):
                s = six.text_type(s, encoding, errors)
            else:
                s = six.text_type(s)
        elif hasattr(s, '__unicode__'):
            s = six.text_type(s)
        else:
            s = six.text_type(bytes(s), encoding, errors)
    else:
        # Note: We use .decode() here, instead of six.text_type(s, encoding,
        # errors), so that if s is a SafeBytes, it ends up being a
        # SafeText at the end.
        s = s.decode(encoding, errors)
    return s

def force_bytes(s, encoding='utf-8', errors='strict'):
    if isinstance(s, six.binary_type):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if not isinstance(s, six.string_types):
        try:
            if six.PY3:
                return six.text_type(s).encode(encoding)
            else:
                return bytes(s)
        except UnicodeEncodeError:
            return six.text_type(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)

if six.PY3:
    force_str = force_text
else:
    force_str = force_bytes
    force_unicode = force_text