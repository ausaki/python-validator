from __future__ import unicode_literals, print_function
from validator import Validator, ListField, DictField, IntegerField, EnumField


class CardValidator(Validator):
    number = IntegerField(min_value=1, max_value=13)
    category = EnumField(choices=['A', 'B', 'C', 'D'])


class CardsValidator(Validator):
    cards = ListField(min_length=1, max_length=52,
                      field=DictField(validator=CardValidator))


def test_ok():
    data = {'cards': [{'number': 1, 'category': 'A'},
                      {'number': 2, 'category': 'B'},
                      {'number': 3, 'category': 'A'}]}
    v = CardsValidator(data)
    assert v.is_valid(), v.str_errors


def test_data():
    data = {'cards': [{'number': 1, 'category': 'A'},
                      {'number': 2, 'category': 'B'},
                      {'number': 3, 'category': 'A'}]}
    v = CardsValidator(data)
    assert v.is_valid(), v.str_errors

    validated_data = v.validated_data
    assert data == validated_data

    data['cards'][0]['number'] = 2
    assert validated_data['cards'][0]['number'] != 2


def test_mock_data():
    data = CardsValidator.mock_data()
    print('cards:', data)
    assert 'cards' in data
    assert 1 <= len(data['cards']) <= 52
