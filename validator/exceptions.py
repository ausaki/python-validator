# -*- coding: utf-8 -*-

class BaseValidationError(Exception):

    default_detail = 'Base validation error'
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        self.detail = detail if detail else self.default_detail
        self.code = code if code else self.default_code
    
    def __str__(self):
        return '({code}, {detail})'.format(code=self.code, detail=self.detail)


class FieldRequiredError(Exception):

    default_detail = 'Field is required'
    default_code = 'error'


class ValidationError(Exception):

    default_detail = 'Validation error'
    default_code = 'error'


class FieldValidationError(Exception):

    default_detail = 'field Validation error'
    default_code = 'error'