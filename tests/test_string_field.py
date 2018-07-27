from validator import Validator, StringField

class V(Validator):
        name = StringField()

def test_ok():
    data = {'name': 'foo'}
    v = V(data)
    assert v.is_valid()


def test_wrong_type():
    data = {'name': 123}
    v = V(data)
    assert not v.is_valid()

    class V2(Validator):
        name = StringField(strict=False)

    data = {'name': 123}
    v = V2(data)
    assert v.is_valid()


def test_empty_string():
    data = {'name': ''}
    v = V(data)
    assert v.is_valid()


def test_size():
    class V(Validator):
        name = StringField(min_length=10, max_length=20)

    data = {'name': 'foo'}
    v = V(data)
    assert not v.is_valid()

    data = {'name': 'foo' * 4}
    v = V(data)
    assert v.is_valid()

    data = {'name': 'foo' * 10}
    v = V(data)
    assert not v.is_valid()


def test_regex():
    class V(Validator):
        name = StringField(regex='^my')

    data = {'name': 'my name is foo'}
    v = V(data)
    assert v.is_valid()


def test_mock_data():
    data = V.mock_data()
    assert 'name' in data
    assert V(data).is_valid()


def test_to_dict():
    data_dict = V.to_dict()
    assert 'name' in data_dict
    field_info = data_dict['name']
    for p in StringField.PARAMS:
        assert p in field_info
    assert field_info['type'] == StringField.FIELD_TYPE_NAME
    assert field_info['min_length'] == 0
    assert field_info['max_length'] is None
    assert field_info['regex'] is None
