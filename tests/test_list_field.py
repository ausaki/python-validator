from validator import Validator, ListField, IntegerField


class CardsValidator(Validator):
    cards = ListField(min_length=1, max_length=52, field=IntegerField(min_value=1, max_value=13))


def test_ok():
    data = {'cards': [1, 2, 3, 4]}
    v = CardsValidator(data)
    assert v.is_valid(), v.str_errors


def test_wrong_type():
    data = {'cards': ''}
    v = CardsValidator(data)
    assert not v.is_valid()


def test_too_many_elements():
    data = {'cards': [1] * 60}
    v = CardsValidator(data)
    assert not v.is_valid()


def test_too_big_elements():
    data = {'cards': [1, 2, 20]}
    v = CardsValidator(data)
    assert not v.is_valid()

def test_data():
    data = {'cards': [1, 2, 3, 4]}
    v = CardsValidator(data)
    assert v.is_valid()

    validated_data = v.validated_data
    assert data == validated_data

    data['cards'][0] = 2
    assert validated_data['cards'][0] != 2


def test_mock_data():
    data = CardsValidator.mock_data()
    print 'cards:', data
    assert 'cards' in data
    assert 1 <= len(data['cards']) <= 52


def test_no_field():
    class CardsValidator(Validator):
        cards = ListField(min_length=1, max_length=52)

    data = {'cards': [1, 2, 3, 4]}
    v = CardsValidator(data)
    assert v.is_valid()

    validated_data = v.validated_data
    assert data == validated_data

    data['cards'][0] = 2
    assert validated_data['cards'][0] != 2

