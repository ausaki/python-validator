from validator import Validator, EmailField


class V(Validator):
        email = EmailField()

def test_ok():
    data = {'email': 'foo@example.com'}
    v = V(data)
    assert v.is_valid()


def test_wrong_value():
    data = {'email': '<foo>@example.com'}
    v = V(data)
    assert not v.is_valid(), v.str_errors


def test_mock_data():
    data = V.mock_data()
    assert 'email' in data
    assert V(data).is_valid()

def test_to_dict():
    data_dict = V.to_dict()
    assert 'email' in data_dict
    field_info = data_dict['email']
    for p in EmailField.PARAMS:
        assert p in field_info
    assert field_info['type'] == EmailField.FIELD_TYPE_NAME
    assert field_info['strict'] == True
    assert field_info['regex'].pattern == EmailField.REGEX