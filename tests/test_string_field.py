from validator import Validator, StringField


def test_ok():
    class V(Validator):
        name = StringField()

    data = {'name': 'foo'}
    v = V(data)
    assert v.is_valid()


def test_wrong_type():
    class V(Validator):
        name = StringField()

    data = {'name': 123}
    v = V(data)
    assert not v.is_valid()

    class V2(Validator):
        name = StringField(strict=False)

    data = {'name': 123}
    v = V2(data)
    assert v.is_valid()


def test_empty_string():
    class V(Validator):
        name = StringField()

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
    class V(Validator):
        name = StringField()

    data = V.mock_data()
    assert 'name' in data
    assert V(data).is_valid()
