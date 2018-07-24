from validator import Validator, URLField


class URLValidator(Validator):
    link = URLField()


def test_ok():
    data = [
        {'link': 'http://www.example.com/'},
        {'link': 'http://user:pass@www.example.com/'},
        {'link': 'http://www.example.com/a/b/c/?a=1&b=2'},
    ]
    for d in data:
        v = URLValidator(d)
        assert v.is_valid()


def test_wrong_value():
    data = [
        {'link': 'abcdef'},
        {'link': 'abc.com/a/b/c'},
    ]
    for d in data:
        v = URLValidator(d)
        assert not v.is_valid()


def test_mock_data():
    data = URLValidator.mock_data()
    assert 'link' in data
    assert URLValidator(data).is_valid()