from validator import Validator, DatetimeField, create_validator


class V(Validator):
        create_at = DatetimeField()

def test_ok():
    data = {'create_at': 1532339910}
    v = V(data)
    assert v.is_valid()

    data = {'create_at': '1532339910'}
    v = V(data)
    assert v.is_valid()


    data = {'create_at': '2018/07/01 17:01:20'}
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
    for p in DatetimeField.PARAMS:
        assert p in field_info
    assert field_info['type'] == DatetimeField.FIELD_TYPE_NAME
    assert field_info['dt_format'] == DatetimeField.DEFAULT_FORMAT


def test_create_valiadtor():
    data = {
        'create_at': {
            'type': 'datetime',
            'dt_format': '%Y/%m/%d %H:%M:%S',
            'tzinfo': 'Asia/Shanghai'
        }
    }
    V = create_validator(data)
    assert issubclass(V, Validator)

    data = {'create_at': '2018/07/01 17:01:20'}
    v = V(data)
    assert v.is_valid(), v.str_errors
    