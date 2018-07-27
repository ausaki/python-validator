# -*- coding: utf-8 -*-
class BaseValidationError(Exception):

    default_detail = 'Base validation error'
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        self.detail = detail if detail else self.default_detail
        self.code = code if code else self.default_code
    
    def __str__(self):
        return self.detail
    
    def __repr__(self):
        detail = self.detail
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