from validator import Validator, BoolField

class V(Validator):
        is_actived = BoolField()

def test_ok():
    data = { 'is_actived': True }
    v = V(data)
    assert v.is_valid()


def test_str_fail():
    data = { 'is_actived': 'True' }
    v = V(data)
    assert not v.is_valid()

def test_str_ok():
    class V(Validator):
        is_actived = BoolField(strict=False)
    
    data = { 'is_actived': 'True' }
    v = V(data)
    assert v.is_valid()


def test_mock_data():
    data = V.mock_data()
    assert 'is_actived' in data
    assert data['is_actived'] in [True, False]


def test_to_dict():
    data = V.to_dict()
    assert 'is_actived' in data
    field_info = data['is_actived']
    assert field_info['type'] == BoolField.FIELD_TYPE_NAME
    


