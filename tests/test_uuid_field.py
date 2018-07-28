import pytest
import uuid
from validator import Validator, UUIDField

class V(Validator):
        uid = UUIDField()

def test_ok():
    data = {'uid': '0'*32}
    v = V(data)
    assert v.is_valid()


def test_wrong_value():
    data = {'uid': '0'*10}
    v = V(data)
    assert not v.is_valid()


def test_uuid_obj():
    data = {'uid': uuid.uuid4()}
    v = V(data)
    assert v.is_valid()


def test_mock_data():
    data = V.mock_data()
    assert 'uid' in data
    assert V(data).is_valid()


def test_to_dict():
    data_dict = V.to_dict()
    assert 'uid' in data_dict
    field_info = data_dict['uid']
    for p in UUIDField.PARAMS:
        assert p in field_info
    assert field_info['type'] == UUIDField.FIELD_TYPE_NAME
    assert field_info['strict'] == False
    assert field_info['format'] == 'hex'


def test_presentation():
    uid = uuid.uuid4()
    value = UUIDField().to_presentation(uid)
    assert value == uid.hex

    value = UUIDField(format='str').to_presentation(uid)
    assert value == str(uid)

    value = UUIDField(format='int').to_presentation(uid)
    assert value == uid.int

    value = UUIDField(format='bytes').to_presentation(uid)
    assert value == uid.bytes

    value = UUIDField(format='bytes_le').to_presentation(uid)
    assert value == uid.bytes_le