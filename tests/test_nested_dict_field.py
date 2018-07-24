from validator import Validator, DictField, IntegerField

class BorderValidator(Validator):
    width = IntegerField()
    color = IntegerField()

class RectangleValidator(Validator):
    width = IntegerField()
    height = IntegerField()
    border = DictField(validator=BorderValidator)

class ShapeValidator(Validator):
    rectangle = DictField(validator=RectangleValidator)


def test_ok():
    data = {'rectangle': {'width': 10, 'height': 50, 'border': {'width': 1, 'color': 0xff0000}}}
    v = ShapeValidator(data)
    assert v.is_valid()


def test_ok_2():
    data = {'rectangle': {}}
    v = ShapeValidator(data)
    assert v.is_valid()


def test_data():
    data = {'rectangle': {'width': 10, 'height': 50, 'border': {'width': 1, 'color': 0xff0000}}}
    v = ShapeValidator(data)
    assert v.is_valid()
    
    validated_data = v.validated_data
    assert data == validated_data

    data['rectangle']['border']['width'] = 2
    assert validated_data['rectangle']['border']['width'] != 2
