from validator import Validator, IPAddressField


class V(Validator):
    ip = IPAddressField()


def test_ok():
    data = [
        {'ip': '127.0.0.1'},
        {'ip': 0x7f000001},
        {'ip': '0x7f000001'},
        {'ip': '::1234:1234'},
    ]
    for d in data:
        v = V(d)
        assert v.is_valid()


def test_wrong_value():
    data = {'ip': '127.0.0.300'}
    v = V(data)
    assert not v.is_valid()


def test_mock_data():
    data = V.mock_data()
    assert 'ip' in data
    assert V(data).is_valid()

def test_to_dict():
    data_dict = V.to_dict()
    assert 'ip' in data_dict
    field_info = data_dict['ip']
    for p in IPAddressField.PARAMS:
        assert p in field_info
    assert field_info['type'] == IPAddressField.FIELD_TYPE_NAME
    assert field_info['version'] == 'both'