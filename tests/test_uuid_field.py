import pytest
import uuid
from validator import Validator, UUIDField


def test_ok():
    class V(Validator):
        uid = UUIDField()

    data = {'uid': '0'*32}
    v = V(data)
    assert v.is_valid()


def test_wrong_value():
    class V(Validator):
        uid = UUIDField()

    data = {'uid': '0'*10}
    v = V(data)
    assert not v.is_valid()


def test_uuid_obj():
    class V(Validator):
        uid = UUIDField()
    data = {'uid': uuid.uuid4()}
    v = V(data)
    assert v.is_valid()


def test_mock_data():
    class V(Validator):
        uid = UUIDField()

    data = V.mock_data()
    assert 'uid' in data
    assert V(data).is_valid()


def test_presentation():
    uid = uuid.uuid4()
    value = UUIDField().to_presentation(uid)
    assert value == uid.get_hex()

    value = UUIDField(format='str').to_presentation(uid)
    assert value == str(uid)

    value = UUIDField(format='int').to_presentation(uid)
    assert value == uid.int

    value = UUIDField(format='bytes').to_presentation(uid)
    assert value == uid.bytes

    value = UUIDField(format='bytes_le').to_presentation(uid)
    assert value == uid.bytes_le