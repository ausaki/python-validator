# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six

def force_text(s):
    if isinstance(s, six.text_type):
        return s
    else:
        try:
            return six.text_type(s)
        except UnicodeDecodeError as e:
            return s
    return s