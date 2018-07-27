from validator import Validator, URLField


class V(Validator):
    link = URLField()


def test_ok():
    data = [
        {'link': 'http://www.example.com/'},
        {'link': 'http://user:pass@www.example.com/'},
        {'link': 'http://www.example.com/a/b/c/?a=1&b=2'},
    ]
    for d in data:
        v = V(d)
        assert v.is_valid()


def test_wrong_value():
    data = [
        {'link': 'abcdef'},
        {'link': 'abc.com/a/b/c'},
    ]
    for d in data:
        v = V(d)
        assert not v.is_valid()


def test_mock_data():
    data = V.mock_data()
    assert 'link' in data
    assert V(data).is_valid()


def test_to_dict():
    data_dict = V.to_dict()
    assert 'link' in data_dict
    field_info = data_dict['link']
    for p in URLField.PARAMS:
        assert p in field_info
    assert field_info['type'] == URLField.FIELD_TYPE_NAME
    assert field_info['strict'] == True
    assert field_info['min_length'] == 0