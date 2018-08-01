# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from validator import StringField, DateField
from validator.fields import FIELDS_NAME_MAP, __all__
from validator.exceptions import FieldValidationError

print(FIELDS_NAME_MAP)
print(__all__)
print(StringField().to_dict())
print(DateField._get_all_params())

e = FieldValidationError()
print(repr(e))