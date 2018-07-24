from validator import Validator, NumberField, IntegerField, FloatField


def test_ok():
    class V(Validator):
        number = NumberField()

    data = {'number': 10}
    v = V(data)
    assert v.is_valid()


def test_wrong_type():
    class V(Validator):
        number = NumberField()

    data = {'number': '10'}
    v = V(data)
    assert not v.is_valid()

    class V2(Validator):
        number = NumberField(strict=False)

    data = {'number': '10'}
    v = V2(data)
    assert v.is_valid()


def test_range():
    class V(Validator):
        number = NumberField(min_value=10, max_value=100)

    data = {'number': 9}
    v = V(data)
    assert not v.is_valid()

    data = {'number': 50}
    v = V(data)
    assert v.is_valid()

    data = {'number': 110}
    v = V(data)
    assert not v.is_valid()


def test_mock_data():
    class V(Validator):
        number = NumberField()

    data = V.mock_data()
    assert 'number' in data
    assert V(data).is_valid()
