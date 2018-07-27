from validator import Validator, MD5Field


class V(Validator):
    md5_hash = MD5Field()


def test_ok():
    data = {'md5_hash': '5'*32}
    v = V(data)
    assert v.is_valid(), v.str_errors


def test_wrong_value():
    data = {'md5_hash': '5'*30}
    v = V(data)
    assert not v.is_valid(), v.str_errors


def test_mock_data():
    data = V.mock_data()
    assert 'md5_hash' in data
    assert V(data).is_valid()


def test_to_dict():
    data_dict = V.to_dict()
    assert 'md5_hash' in data_dict
    field_info = data_dict['md5_hash']
    for p in MD5Field.PARAMS:
        assert p in field_info
    assert field_info['type'] == MD5Field.FIELD_TYPE_NAME
    assert field_info['min_length'] == 32
    assert field_info['max_length'] == 32
