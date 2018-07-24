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

