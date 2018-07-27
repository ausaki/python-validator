from validator import Validator, DictField, IntegerField, create_validator

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


def test_create_valiadtor():
    data = {
        'rectangle': {
            'type': 'dict',
            'validator': {
                'width': {
                    'type': 'integer',
                },
                'height': {
                    'type': 'integer',
                },
                'border': {
                    'type': 'dict',
                    'validator': {
                        'width': {
                            'type': 'integer'
                        },
                        'color': {
                            'type': 'integer'
                        }
                    }
                }
            },
        }
    }
    V = create_validator(data)
    assert issubclass(V, Validator)

    data = {'rectangle': {'width': 10, 'height': 50, 'border': {'width': 1, 'color': 0xff0000}}}
    v = V(data)
    assert v.is_valid()