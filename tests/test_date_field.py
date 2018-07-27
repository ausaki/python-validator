from validator import Validator, DateField


class V(Validator):
        create_at = DateField()

def test_ok():
    data = {'create_at': 1532339910}
    v = V(data)
    assert v.is_valid()

    data = {'create_at': '1532339910'}
    v = V(data)
    assert v.is_valid()


    data = {'create_at': '2018/07/01'}
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
    print DateField.PARAMS
    print field_info
    for p in DateField.PARAMS:
        assert p in field_info, field_info
    assert field_info['type'] == DateField.FIELD_TYPE_NAME
    assert field_info['dt_format'] == DateField.DEFAULT_FORMAT

