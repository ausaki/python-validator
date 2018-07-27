from validator import Validator, TimestampField


class V(Validator):
        create_at = TimestampField()

def test_ok():
    data = {'create_at': 1532339910}
    v = V(data)
    assert v.is_valid()


def test_wrong_value():
    data = {'create_at': 'abc'}
    v = V(data)
    assert not v.is_valid(), v.str_errors


def test_mock_data():
    data = V.mock_data()
    assert 'create_at' in data
    assert V(data).is_valid()

def test_to_dict():
    data_dict = V.to_dict()
    assert 'create_at' in data_dict
    field_info = data_dict['create_at']
    for p in TimestampField.PARAMS:
        assert p in field_info
    assert field_info['type'] == TimestampField.FIELD_TYPE_NAME
    assert field_info['min_value'] == 0
    assert field_info['max_value'] == 2 ** 32 - 1

