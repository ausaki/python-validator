from validator import Validator, MD5Field


def test_ok():
    class V(Validator):
        md5_hash = MD5Field()

    data = {'md5_hash': '5'*32}
    v = V(data)
    assert v.is_valid(), v.str_errors


def test_wrong_value():
    class V(Validator):
        md5_hash = MD5Field()

    data = {'md5_hash': '5'*30}
    v = V(data)
    assert not v.is_valid(), v.str_errors


def test_mock_data():
    class V(Validator):
        md5_hash = MD5Field()

    data = V.mock_data()
    assert 'md5_hash' in data
    assert V(data).is_valid()
