from validator import Validator, IPAddressField


class IPAddressValidator(Validator):
    ip = IPAddressField()


def test_ok():
    data = [
        {'ip': '127.0.0.1'},
        {'ip': 0x7f000001},
        {'ip': '0x7f000001'},
        {'ip': '::1234:1234'},
    ]
    for d in data:
        v = IPAddressValidator(d)
        assert v.is_valid()


def test_wrong_value():
    data = {'ip': '127.0.0.300'}
    v = IPAddressValidator(data)
    assert not v.is_valid()


def test_mock_data():
    data = IPAddressValidator.mock_data()
    assert 'ip' in data
    assert IPAddressValidator(data).is_valid()