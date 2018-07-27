from validator import Validator, ListField, IntegerField, create_validator


class V(Validator):
    cards = ListField(min_length=1, max_length=52,
                      field=IntegerField(min_value=1, max_value=13))


def test_ok():
    data = {'cards': [1, 2, 3, 4]}
    v = V(data)
    assert v.is_valid(), v.str_errors


def test_wrong_type():
    data = {'cards': ''}
    v = V(data)
    assert not v.is_valid()


def test_too_many_elements():
    data = {'cards': [1] * 60}
    v = V(data)
    assert not v.is_valid()


def test_too_big_elements():
    data = {'cards': [1, 2, 20]}
    v = V(data)
    assert not v.is_valid()


def test_data():
    data = {'cards': [1, 2, 3, 4]}
    v = V(data)
    assert v.is_valid()

    validated_data = v.validated_data
    assert data == validated_data

    data['cards'][0] = 2
    assert validated_data['cards'][0] != 2


def test_mock_data():
    data = V.mock_data()
    print 'cards:', data
    assert 'cards' in data
    assert 1 <= len(data['cards']) <= 52


def test_to_dict():
    data_dict = V.to_dict()
    assert 'cards' in data_dict
    field_info = data_dict['cards']
    for p in ListField.PARAMS:
        assert p in field_info
    assert field_info['type'] == ListField.FIELD_TYPE_NAME
    assert isinstance(field_info['field'], dict)
    assert field_info['min_length'] == 1
    assert field_info['max_length'] == 52


def test_create_valiadtor():
    data = {
        'cards': {
            'type': 'list',
            'field': {
                'type': 'integer',
                'min_value': 1,
                'max_value': 13
            },
            'min_length': 1,
            'max_length': 52
        }
    }
    V = create_validator(data)
    assert issubclass(V, Validator)

    data = {'cards': [1, 2, 3, 4]}
    v = V(data)
    assert v.is_valid()

def test_no_field():
    class V(Validator):
        cards = ListField(min_length=1, max_length=52)

    data = {'cards': [1, 2, 3, 4]}
    v = V(data)
    assert v.is_valid()

    validated_data = v.validated_data
    assert data == validated_data

    data['cards'][0] = 2
    assert validated_data['cards'][0] != 2
