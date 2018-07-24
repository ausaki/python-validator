from validator import Validator, SHAField


def test_ok():
    class V(Validator):
        sha_hash = SHAField()

    data = {'sha_hash': '5'*64}
    v = V(data)
    assert v.is_valid(), v.format_errors

    class V2(Validator):
        sha_hash = SHAField(version=512)

    data = {'sha_hash': '5'*128}
    v = V2(data)
    assert v.is_valid(), v.format_errors


def test_wrong_value():
    class V(Validator):
        sha_hash = SHAField()

    data = {'sha_hash': '5'*30}
    v = V(data)
    assert not v.is_valid(), v.format_errors


def test_mock_data():
    class V(Validator):
        sha_hash = SHAField()

    data = V.mock_data()
    assert 'sha_hash' in data
    assert V(data).is_valid()
