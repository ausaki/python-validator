# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from validator import FieldValidationError
from validator.translation import gettext
from validator.utils import force_text
import os
import pytest

languages = os.environ.get('PYTHON_VALIDATOR_LANGUAGES')


@pytest.mark.skipif(languages != 'en', reason='PYTHON_VALIDATOR_LANGUAGES = {}'.format(languages))
def test_en_translation():
    assert force_text(gettext('error')) == 'error'


@pytest.mark.skipif(languages != 'zh_CN', reason='PYTHON_VALIDATOR_LANGUAGES = {}'.format(languages))
def test_zh_cn_translation():
    assert force_text(gettext('error')) == '错误'
