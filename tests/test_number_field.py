from validator import Validator, NumberField, IntegerField, FloatField

class V(Validator):
        number = NumberField()

def test_ok():
    data = {'number': 10}
    v = V(data)
    assert v.is_valid()


def test_wrong_type():
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
    data = V.mock_data()
    assert 'number' in data
    assert V(data).is_valid()



def test_to_dict():
    data_dict = V.to_dict()
    assert 'number' in data_dict
    field_info = data_dict['number']
    for p in NumberField.PARAMS:
        assert p in field_info
    assert field_info['type'] == NumberField.FIELD_TYPE_NAME
    assert field_info['min_value'] is None
    assert field_info['max_value'] is None
