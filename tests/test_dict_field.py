from validator import Validator, DictField, IntegerField


class RectangleValidator(Validator):
    width = IntegerField()
    height = IntegerField()


class ShapeValidator(Validator):
    rectangle = DictField(validator=RectangleValidator)


def test_ok():
    data = {'rectangle': {'width': 10, 'height': 50}}
    v = ShapeValidator(data)
    assert v.is_valid()


def test_ok_2():
    data = {'rectangle': {}}
    v = ShapeValidator(data)
    assert v.is_valid()


def test_wrong_type():
    data = {'rectangle': ''}
    v = ShapeValidator(data)
    assert not v.is_valid()


def test_data():
    data = {'rectangle': {'width': 10, 'height': 50}}
    v = ShapeValidator(data)
    assert v.is_valid()

    validated_data = v.validated_data
    assert data == validated_data

    data['rectangle']['width'] = 20
    assert validated_data['rectangle']['width'] != 20


def test_mock_data():
    data = ShapeValidator.mock_data()
    print 'shape:', data
    assert 'rectangle' in data
    assert 'width' in data['rectangle']
    assert 'height' in data['rectangle']


def test_to_dict():
    data_dict = ShapeValidator.to_dict()
    assert 'rectangle' in data_dict
    field_info = data_dict['rectangle']
    for p in DictField.PARAMS:
        assert p in field_info
    assert field_info['type'] == DictField.FIELD_TYPE_NAME


def test_no_validator():
    class ShapeValidator(Validator):
        rectangle = DictField()

    data = {'rectangle': {'width': 10, 'height': 50}}
    v = ShapeValidator(data)
    assert v.is_valid()

    validated_data = v.validated_data
    assert data == validated_data

    data['rectangle']['width'] = 20
    assert validated_data['rectangle']['width'] != 20
