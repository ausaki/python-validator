from validator import Validator, StringField, IntegerField, EnumField, FieldValidationError, ValidationError


def test_custom_field_validator():
    class V(Validator):
        name = StringField(max_length=50, required=True)
        age = IntegerField(min_value=1, max_value=120, default=20)
        sex = EnumField(choices=['f', 'm'])

        def validate_name(self, value):
            if value == 'foo':
                raise FieldValidationError('"foo" is invalid')

    data = {
        'name': 'Bob',
        'age': 30,
        'sex': 'm'
    }
    v = V(data)
    assert v.is_valid()

    data['name'] = 'foo'
    v = V(data)
    assert not v.is_valid()


def test_custom_global_validator():
    class V(Validator):
        name = StringField(max_length=50, required=True)
        age = IntegerField(min_value=1, max_value=120, default=20)
        sex = EnumField(choices=['f', 'm'])

        def validate(self, data):
            if data['name'] == 'foo' and data['age'] < 30:
                raise ValidationError('foo is too young, he is older than 30')
    
    data = {
        'name': 'Bob',
        'age': 20,
        'sex': 'm'
    }
    v = V(data)
    assert v.is_valid()

    data['name'] = 'foo'
    v = V(data)
    assert not v.is_valid()


def test_missed_field():
    class V(Validator):
        name = StringField(max_length=50, required=True)
        age = IntegerField(min_value=1, max_value=120)
        sex = EnumField(choices=['f', 'm'])
    
    data = {
        'name': 'Bob',
        'sex': 'm'
    }
    v = V(data)
    v.is_valid()
    assert 'age' not in v.validated_data
