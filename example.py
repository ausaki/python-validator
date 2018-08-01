# -*- coding: utf-8 -*-
from __future__ import print_function
from validator import Validator, StringField, IntegerField, EnumField, ListField, DictField, create_validator
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
print('正确数据')
print('data: ', data)
print('is_valid:', v.is_valid())
print('errors:', v.errors)
print('validated_data:', v.validated_data)


data = {
    'age': '24',
    'sex': 'f'
}
v = UserInfoValidator(data)
print('错误数据')
print('data: ', data)
print('is_valid:', v.is_valid())
print('errors:', v.errors['age'])
print('str_errors:', v.str_errors)
print('validated_data:', v.validated_data)

data = {
    'name': 'abc' * 20,
    'age': 24,
    'sex': 'f'
}
v = UserInfoValidator(data)
print('错误数据')
print('data: ', data)
print('is_valid:', v.is_valid())
print('errors:', v.str_errors)
print('validated_data:', v.validated_data)


data = {
    'name': 'Michael',
    'age': 24,
    'sex': 'c'
}
v = UserInfoValidator(data)
print('错误数据')
print('data: ', data)
print('is_valid:', v.is_valid())
print('errors:', v.str_errors)
print('validated_data:', v.validated_data)

data = UserInfoValidator.mock_data()
print('mock_data:', data)

print('to_dict:')
pprint.pprint(UserInfoValidator.to_dict())


# ListField dict

class V(Validator):
    cards = ListField(min_length=1, max_length=52,
                      field=IntegerField(min_value=1, max_value=13))


print(json.dumps(V.to_dict(), indent=4))


V = create_validator(V.to_dict())
print(json.dumps(V.to_dict(), indent=4))


data = {
    'rectangle': {
        'type': 'dict',
        'validator': {
            'width': {
                'type': 'integer',
                'default': '__empty__'
            },
            'height': {
                'type': 'integer',
            }
        },
    }
}
V = create_validator(data)
print(json.dumps(V.to_dict(), indent=4))
