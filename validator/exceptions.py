# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six
from .utils import force_text


def _flat_error_detail(detail):
    if isinstance(detail, list):
        return [_flat_error_detail(item) for item in detail]
    elif isinstance(detail, dict):
        return {
            key: _flat_error_detail(value)
            for key, value in six.iteritems(detail)
        }
    else:
        return force_text(detail)


class BaseValidationError(Exception):

    default_detail = 'Base validation error'
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        """
        :param detail: `detail` maybe a string, a dict or a list.
        :param code: error code, it not used for now.
        """
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _flat_error_detail(detail)
        self.code = code

    def get_detail(self):
        return self.detail

    def __str__(self):
        return force_text(self.detail)
    
    def __unicode__(self):
        return force_text(self.detail)

    def __repr__(self):
        detail = force_text(self.detail)
        if len(detail) > 103:
            detail = detail[:100] + '...'
        return '<{0}: {1}>'.format(self.__class__.__name__, detail)


class FieldRequiredError(BaseValidationError):

    default_detail = 'Field is required'
    default_code = 'error'


class ValidationError(BaseValidationError):

    default_detail = 'Validation error'
    default_code = 'error'


class FieldValidationError(BaseValidationError):

    default_detail = 'field Validation error'
    default_code = 'error'
