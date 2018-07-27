from validator import Validator, SHAField

class V(Validator):
        sha_hash = SHAField()

def test_ok():
    data = {'sha_hash': '5'*64}
    v = V(data)
    assert v.is_valid(), v.format_errors

    class V2(Validator):
        sha_hash = SHAField(version=512)

    data = {'sha_hash': '5'*128}
    v = V2(data)
    assert v.is_valid(), v.format_errors


def test_wrong_value():
    data = {'sha_hash': '5'*30}
    v = V(data)
    assert not v.is_valid(), v.format_errors


def test_mock_data():
    data = V.mock_data()
    assert 'sha_hash' in data
    assert V(data).is_valid()

def test_to_dict():
    data_dict = V.to_dict()
    assert 'sha_hash' in data_dict
    field_info = data_dict['sha_hash']
    for p in SHAField.PARAMS:
        assert p in field_info
    assert field_info['type'] == SHAField.FIELD_TYPE_NAME
    assert field_info['version'] == 256