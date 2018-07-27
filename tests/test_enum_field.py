import pytest
from validator import Validator, EnumField


def test_empty_choices():
    with pytest.raises(ValueError):
        class V(Validator):
            number = EnumField()


class V(Validator):
    number = EnumField(choices=[1, 2, 3])


def test_ok():
    data = {'number': 1}
    v = V(data)
    assert v.is_valid()


def test_wrong_value():
    data = {'number': 10}
    v = V(data)
    assert not v.is_valid()


def test_mock_data():
    data = V.mock_data()
    assert 'number' in data
    assert V(data).is_valid()


def test_to_dict():
    data_dict = V.to_dict()
    assert 'number' in data_dict
    field_info = data_dict['number']
    for p in EnumField.PARAMS:
        assert p in field_info
    assert field_info['type'] == EnumField.FIELD_TYPE_NAME
    assert field_info['choices'] == [1, 2, 3]
