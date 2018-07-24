import pytest
from validator import Validator, EnumField


def test_empty_choices():
    with pytest.raises(ValueError):
        class V(Validator):
            number = EnumField()


def test_ok():
    class V(Validator):
        number = EnumField(choices=[1, 2, 3])

    data = {'number': 1}
    v = V(data)
    assert v.is_valid()


def test_wrong_value():
    class V(Validator):
        number = EnumField(choices=[1, 2, 3])

    data = {'number': 10}
    v = V(data)
    assert not v.is_valid()


def test_mock_data():
    class V(Validator):
        number = EnumField(choices=[1, 2, 3])

    data = V.mock_data()
    assert 'number' in data
    assert V(data).is_valid()
