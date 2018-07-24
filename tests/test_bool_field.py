from validator import Validator, BoolField

def test_ok():
    class V(Validator):
        is_actived = BoolField()
    
    data = { 'is_actived': True }
    v = V(data)
    assert v.is_valid()


def test_str_fail():
    class V(Validator):
        is_actived = BoolField()
    
    data = { 'is_actived': 'True' }
    v = V(data)
    assert not v.is_valid()

def test_str_ok():
    class V(Validator):
        is_actived = BoolField(strict=False)
    
    data = { 'is_actived': 'True' }
    v = V(data)
    assert v.is_valid()

