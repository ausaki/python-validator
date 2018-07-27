# -*- coding: utf-8 -*-

from validator import Validator, StringField, IntegerField, EnumField
from validator.exceptions import FieldRequiredError
import json
import pprint

class UserInfoValidator(Validator):
    name = StringField(max_length=50, required=True)
    age = IntegerField(min_value=1, max_value=120, default=20)
    sex = EnumField(choices=['f', 'm'])


data = {
    'name': 'Michael',
    'age': 24,
    'sex': 'f'
}
v = UserInfoValidator(data)
print '正确数据'
print 'data: ', data
print 'is_valid:', v.is_valid()
print 'errors:', v.errors
print 'validated_data:', v.validated_data


data = {
    'age': '24',
    'sex': 'f'
}
v = UserInfoValidator(data)
print '错误数据'
print 'data: ', data
print 'is_valid:', v.is_valid()
print 'errors:', v.errors
print 'str_errors:', v.str_errors
print 'validated_data:', v.validated_data

data = {
    'name': 'abc' * 20,
    'age': 24,
    'sex': 'f'
}
v = UserInfoValidator(data)
print '错误数据'
print 'data: ', data
print 'is_valid:', v.is_valid()
print 'errors:', v.str_errors
print 'validated_data:', v.validated_data


data = {
    'name': 'Michael',
    'age': 24,
    'sex': 'c'
}
v = UserInfoValidator(data)
print '错误数据'
print 'data: ', data
print 'is_valid:', v.is_valid()
print 'errors:', v.str_errors
print 'validated_data:', v.validated_data

data = UserInfoValidator.mock_data()
print 'mock_data:', data

print 'to_dict:'
pprint.pprint(UserInfoValidator.to_dict())