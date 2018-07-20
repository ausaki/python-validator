# -*- coding: utf-8 -*-
import six
import random
import string
import sys
from . import exceptions


__all__ = [
    'BaseField',
    'StringField',
    'NumberField',
    'IntegerField',
    'FloatField',
    'EnumField',
]


class UniversalInternalType(object):
    """
    this class dont create its own instance, but return the `obj` directly
    """
    def __new__(cls, obj, *args, **kwargs):
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return 'UniversalInternalType'


class BaseField(object):
    """ 
    BaseField
    """

    """
    INTERNAL_TYPE is the type of the field in python internal, like str, int, list, dict
    INTERNAL_TYPE can be a type list, such as [int, long]
    INTERNAL_TYPE used to validate field's type by isinstance(value, INTERNAL_TYPE)
    """
    INTERNAL_TYPE = UniversalInternalType

    def __init__(self, strict=True, default=None, validators=None, required=False, **kwargs):
        self.strict = strict
        self.default = default

        if validators is None:
            validators = []
        elif not isinstance(validators, (tuple, list)):
            validators = [validators]
        self.validators = validators

        self.required = required

    def validate(self, value):
        """
        return validated value or raise FieldValidationError.
        """
        value = self._validate(value)
        for v in self.validators:
            v(value)
        return value

    def _validate(self, value):
        """
        return validated value or raise FieldValidationError.
        sub-class should override this method.
        """
        return value

    @classmethod
    def _convert_type(cls, value):
        if isinstance(cls.INTERNAL_TYPE, (tuple, list)):
            for t in cls.INTERNAL_TYPE:
                try:
                    value = t(value)
                    break
                except TypeError as e:
                    pass
            else:
                raise ValueError()
        else:
            value = cls.INTERNAL_TYPE(value)
        return value

    def _validate_type(self, value):
        """
        validate the type of value
        """
        if self.strict:
            if not isinstance(value, self.INTERNAL_TYPE):
                raise exceptions.FieldValidationError(
                    'Got a wrong type: {}'.format(type(value).__name__))
        else:
            try:
                value = self._convert_type(value)
            except ValueError as e:
                raise exceptions.FieldValidationError(
                    'Type convertion is failed: {}'.format(type(value).__name__))
        return value

    @classmethod
    def _check_value_range(cls, min_value, max_value):
        if max_value is not None and max_value < min_value:
            raise ValueError('the max_value must greater than or equals the min_value, got min_value={min}, max_value={max}'.format(
                min=min_value, max=max_value))

    def is_required(self):
        return self.required

    def get_default(self):
        return self.default

    def to_presentation(self, value):
        return value

    def to_internal(self, value):
        return value

    def mock_data(self):
        return 'this field doesnt implement mock_data method'


class StringField(BaseField):
    """
    StringField
    internal: six.string_types
    presentation: string
    """
    if six.PY2:
        INTERNAL_TYPE = (unicode, str)
    else:
        INTERNAL_TYPE = str

    def __init__(self, min_length=0, max_length=None, **kwargs):
        if min_length < 0:
            min_length = 0
        self._check_value_range(min_length, max_length)
        self.min_length = min_length
        self.max_length = max_length

        super(StringField, self).__init__(**kwargs)

    def _validate(self, value):
        value = self._validate_type(value)

        if len(value) < self.min_length:
            raise exceptions.FieldValidationError(
                'string is too short, min-lenght is {}'.format(self.min_length))
        if self.max_length and len(value) > self.max_length:
            raise exceptions.FieldValidationError(
                'string is too long, max-lenght is {}'.format(self.max_length))
        return value

    def to_internal(self, value):
        return six.text_type(value)

    def mock_data(self):
        min_ = self.min_length
        max_ = self.max_length
        if max_ is None:
            max_ = min_ + 100
        size = random.randint(min_, max_)
        random_str = ''.join(
            [random.choice(string.letters + string.digits) for _ in xrange(size)])
        random_str = self.to_internal(random_str)
        return random_str


class NumberField(BaseField):
    if six.PY2:
        INTERNAL_TYPE = (int, long, float)
    else:
        INTERNAL_TYPE = (int, float)

    def __init__(self, min_value=None, max_value=None, **kwargs):
        self._check_value_range(min_value, max_value)
        self.min_value = min_value
        self.max_value = max_value

        super(NumberField, self).__init__(**kwargs)

    def _validate(self, value):
        value = self._validate_type(value)

        if self.min_value is not None and value < self.min_value:
            raise exceptions.FieldValidationError(
                'value is too small, min-value is {}'.format(self.min_value))

        if self.max_value is not None and value > self.max_value:
            raise exceptions.FieldValidationError(
                'value is too big, max-value is {}'.format(self.max_value))

        return value

    def mock_data(self):
        min_ = self.min_value
        if min_ is None:
            min_ = 0
        max_ = self.max_value
        if max_ is None:
            max_ = min_ + 1000
        return random.uniform(min_, max_)


class IntegerField(NumberField):
    INTERNAL_TYPE = int

    def mock_data(self):
        d = super(IntegerField, self).mock_data()
        return int(d)


class FloatField(NumberField):
    INTERNAL_TYPE = float


class EnumField(BaseField):

    def __init__(self, choices=None, **kwargs):
        if choices is None or len(choices) == 0:
            raise ValueError('choices cant be empty or None')
        self.choices = choices
        kwargs.setdefault('default', choices[0])
        super(EnumField, self).__init__(**kwargs)

    def _validate(self, value):
        if value not in self.choices:
            raise exceptions.FieldValidationError(
                '{} not in the choices'.format(value))
        return value

    def mock_data(self):
        return random.choice(self.choices)
