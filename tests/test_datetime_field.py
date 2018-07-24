from validator import Validator, DatetimeField


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

