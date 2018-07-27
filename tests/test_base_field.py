"""
test common params:
- required
- default value
- strict
- validators
"""

from validator import Validator, BaseField
from validator.exceptions import FieldValidationError


def test_not_required():
    class V(Validator):
        name = BaseField()

    data = {}
    v = V(data)
    assert v.is_valid()


def test_required():
    class V(Validator):
        name = BaseField(required=True)

    data = {}
    v = V(data)
    assert not v.is_valid()


def test_default():
    class V(Validator):
        name = BaseField(default='default_value')

    data = {}
    v = V(data)
    assert v.is_valid(), v.format_errors
    assert v.validated_data['name'] == 'default_value'


def test_strict():
    class V(Validator):
        name = BaseField()

    data = {'name': 'foo'}
    v = V(data)
    assert v.is_valid()


def test_not_strict():
    class V(Validator):
        name = BaseField(strict=False)

    data = {'name': 'foo'}
    v = V(data)
    assert v.is_valid()


def test_validators():
    def validate(value):
        raise FieldValidationError('field is invalid')

    class V(Validator):
        name = BaseField(strict=False, validators=[validate])

    data = {'name': 'foo'}
    v = V(data)
    assert not v.is_valid()
