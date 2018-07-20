from __future__ import unicode_literals
import pytest
from validator import (Validator, StringField, IntegerField, EnumField)
from validator.exceptions import ValidationError


@pytest.fixture(scope='module')
def person_info_validator():

    class PersonInfoValidator(Validator):
        name = StringField(max_length=50, required=True)
        age = IntegerField(min_value=1, max_value=120)
        sex = EnumField(choices=['f', 'm'])

    return PersonInfoValidator


def test_valid_data(person_info_validator):
    data = {
        'name': 'Bob',
        'age': 20,
        'sex': 'f'
    }
    v = person_info_validator(data)
    assert v.is_valid(), v.errors
    assert isinstance(v.validated_data, dict)
    assert v.validated_data['name'] == 'Bob'
    assert v.validated_data['age'] == 20


def test_wrong_type_age(person_info_validator):
    data = {
        'name': 'Bob',
        'age': 'abc'
    }
    v = person_info_validator(data)
    assert not v.is_valid(), v.errors
    assert 'age' in v.errors


def test_too_big_age(person_info_validator):
    data = {
        'name': 'Bob',
        'age': 1000
    }
    v = person_info_validator(data)
    assert not v.is_valid(), v.errors
    assert 'age' in v.errors


def test_empty_name(person_info_validator):
    data = {
        'name': '',
        'age': 10
    }
    v = person_info_validator(data)
    assert v.is_valid(), v.errors


def test_not_provide_name(person_info_validator):
    data = {
        'age': 20
    }
    v = person_info_validator(data)
    assert not v.is_valid(), v.errors
    assert 'name' in v.errors


def test_not_provide_age(person_info_validator):
    data = {
        'name': '',
    }
    v = person_info_validator(data)
    assert v.is_valid(), v.errors


def test_wrong_sex(person_info_validator):
    data = {
        'name': 'Michael',
        'age': 20,
        'sex': 'c'
    }
    v = person_info_validator(data)
    assert not v.is_valid(), v.errors


def test_mock_data(person_info_validator):
    data = person_info_validator.mock_data()
    assert 'name' in data
    assert 'age' in data
    v = person_info_validator(data)
    assert v.is_valid(), v.errors


def test_model_level_validate(person_info_validator):
    class TestValidator(person_info_validator):

        def validate(self, data):
            if data['name'] == 'Lucas' and data['age'] < 10:
                raise ValidationError('Lucas\'s age must greater than 10')
            return data

    data = {
        'name': 'Lucas',
        'age': 20,
        'sex': 'f'
    }
    v = TestValidator(data)
    assert v.is_valid(), v.errors

    data['age'] = 8
    v = TestValidator(data)
    assert not v.is_valid(), v.errors
