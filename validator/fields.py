# -*- coding: utf-8 -*-
import six
import random
import string
import sys
import uuid
import re
import copy
import datetime
from . import exceptions


__all__ = [
    'BaseField',
    'StringField',
    'NumberField',
    'IntegerField',
    'FloatField',
    'BoolField',
    'UUIDField',
    'MD5Field',
    'SHAField',
    'EmailField',
    'EnumField',
    'DictField',
    'ListField',
    'TimestampField',
    'DatetimeField',
    'DateField',
]


class EmptyValue(object):
    """
    a data type replace None
    """

    def __init__(self):
        pass

    def __str__(self):
        return '__empty_value__'


EMPTY_VALUE = EmptyValue()


class BaseField(object):
    """ 
    BaseField
    """

    """
    INTERNAL_TYPE is the type of the field in python internal, like str, int, list, dict
    INTERNAL_TYPE can be a type list, such as [int, long]
    INTERNAL_TYPE used to validate field's type by isinstance(value, INTERNAL_TYPE)
    """
    INTERNAL_TYPE = object

    FIELD_TYPE_NAME = 'object'

    PARAMS = [
        'strict', 'default', 'validators', 'required'
    ]

    def __init__(self, strict=True, default=EMPTY_VALUE, validators=None, required=False, **kwargs):
        """
        :param strict: bool, if strict is True, value must be an instance of INTERVAL_TYPE,
                        otherwise, value should be convert to INTERNAL_TYPE
        :param default: default value, defaults to EMPTY_VALUE
        :param validators: a validator list, validator can be function, other callable object or object that have method named validate 
        :param required: bool, indicate that this field is whether required
        """
        self.strict = strict
        self.default = default

        if validators is None:
            validators = []
        elif not isinstance(validators, (tuple, list)):
            validators = [validators]
        self.validators = validators

        self.required = required

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    def _check_value_range(cls, min_value, max_value):
        if max_value is not None and max_value < min_value:
            raise ValueError('the max value must greater than or equals the min value, got min value={min}, max value={max}'.format(
                min=min_value, max=max_value))

    def _convert_type(self, value):
        if isinstance(self.INTERNAL_TYPE, (tuple, list)):
            for t in self.INTERNAL_TYPE:
                try:
                    value = t(value)
                    break
                except TypeError as e:
                    pass
            else:
                raise ValueError()
        else:
            value = self.INTERNAL_TYPE(value)
        return value

    @property
    def _params(self):
        params = {}
        for name in self.PARAMS:
            if hasattr(self, name):
                params[name] = getattr(self, name)
        return params

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
        return self._validate_type(value)

    def _validate_type(self, value):
        """
        validate the type of value
        """
        if not isinstance(value, self.INTERNAL_TYPE):
            if self.strict:
                raise exceptions.FieldValidationError(
                    'got a wrong type: {0}, expect {1}'.format(type(value).__name__, self.FIELD_TYPE_NAME))
            else:
                try:
                    value = self._convert_type(value)
                except (ValueError, TypeError) as e:
                    raise exceptions.FieldValidationError(
                        'type convertion is failed: {0} -> {1}'.format(type(value).__name__, self.FIELD_TYPE_NAME))
        return value

    def is_required(self):
        return self.required

    def get_default(self):
        """
        return default value
        """
        if callable(self.default):
            return self.default()
        else:
            return self.default

    def to_presentation(self, value):
        """
        value: must be a internal value
        """
        return value

    def to_internal(self, value):
        """
        value: must be a validated value
        """
        return value

    def to_dict(self):
        """
        to dict presentation
        """
        d = {
            'type': self.FIELD_TYPE_NAME,
        }
        d.update(self._params)
        return d

    def mock_data(self):
        """
        reutrn mocking data
        sub-class should override this method
        """
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

    FIELD_TYPE_NAME = 'string'

    def __init__(self, min_length=0, max_length=None, regex=None, **kwargs):
        if min_length < 0:
            min_length = 0
        self._check_value_range(min_length, max_length)
        self.min_length = min_length
        self.max_length = max_length

        if regex is not None:
            regex = re.compile(regex)
        self.regex = regex

        super(StringField, self).__init__(**kwargs)

    def _validate(self, value):
        value = self._validate_type(value)

        if len(value) < self.min_length:
            raise exceptions.FieldValidationError(
                'string is too short, min-lenght is {}'.format(self.min_length))
        if self.max_length and len(value) > self.max_length:
            raise exceptions.FieldValidationError(
                'string is too long, max-lenght is {}'.format(self.max_length))

        if not self._match(value):
            raise exceptions.FieldValidationError(
                '{0} not match {1}'.format(self.regex.pattern, value))

        return value

    def _match(self, value):
        if self.regex is None:
            return True
        else:
            return self.regex.match(value) is not None

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

    FIELD_TYPE_NAME = 'number'

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

    FIELD_TYPE_NAME = 'integer'

    def mock_data(self):
        d = super(IntegerField, self).mock_data()
        return int(d)


class FloatField(NumberField):
    INTERNAL_TYPE = float

    FIELD_TYPE_NAME = 'float'


class BoolField(BaseField):
    INTERNAL_TYPE = bool
    FIELD_TYPE_NAME = 'bool'

    def mock_data(self, value):
        return random.choice([True, False])


class UUIDField(BaseField):
    INTERNAL_TYPE = uuid.UUID
    FIELD_TYPE_NAME = 'UUID'
    SUPPORT_FORMATS = {
        'hex': 'hex',
        'str': '__str__',
        'int': 'int',
        'bytes': 'bytes',
        'bytes_le': 'bytes_le'
    }

    def __init__(self, format='hex', **kwargs):
        """
        format: what format used when to_presentation, supports 'hex', 'str', 'int', 'bytes', 'bytes_le'
        """
        if format not in self.SUPPORT_FORMATS:
            raise ValueError('not supports format: {}'.format(format))
        self.format = format

        kwargs.setdefault('strict', False)
        super(UUIDField, self).__init__(**kwargs)

    def _validate(self, value):
        value = self._validate_type(value)
        return value

    def to_presentation(self, value):
        assert isinstance(value, self.INTERNAL_TYPE)
        attr = getattr(value, self.SUPPORT_FORMATS[self.format])
        if callable(attr):
            return attr()
        return attr

    def mock_data(self):
        return uuid.uuid4()


class MD5Field(StringField):
    FIELD_TYPE_NAME = 'md5'

    def __init__(self, **kwargs):
        kwargs['strict'] = True
        super(MD5Field, self).__init__(min_length=32,
                                       max_length=32,
                                       regex=r'[\da-fA-F]{32}',
                                       **kwargs)

    def _validate(self, value):
        try:
            return super(MD5Field, self)._validate(value)
        except exceptions.FieldValidationError as e:
            raise exceptions.FieldValidationError(
                'Got wrong md5 value: {}'.format(value))

    def mock_data(self):
        return ''.join([random.choice(string.hexdigits) for i in range(32)])


class SHAField(StringField):
    FIELD_TYPE_NAME = 'sha'
    SUPPORT_VERSION = [1, 224, 256, 384, 512]

    def __init__(self, version=256, **kwargs):
        if version not in self.SUPPORT_VERSION:
            raise ValueError('{0} not support, support versions are: {1}'.format(
                version, self.SUPPORT_VERSION))
        if version == 1:
            length = 40
        else:
            length = version / 8 * 2
        self.version = version
        self.length = length
        kwargs['strict'] = True
        super(SHAField, self).__init__(min_length=length,
                                       max_length=length,
                                       regex=r'[\da-fA-F]{' +
                                       str(length) + '}',
                                       **kwargs)

    def _validate(self, value):
        try:
            return super(SHAField, self)._validate(value)
        except exceptions.FieldValidationError as e:
            raise exceptions.FieldValidationError(
                'Got wrong sha{0} value: {1}'.format(self.version, value))

    def mock_data(self):
        return ''.join([random.choice(string.hexdigits) for i in range(self.length)])


class EmailField(StringField):
    FIELD_TYPE_NAME = 'email'
    REGEX = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'

    def __init__(self, **kwargs):
        kwargs['strict'] = True
        super(EmailField, self).__init__(regex=self.REGEX, **kwargs)

    def _validate(self, value):
        try:
            return super(EmailField, self)._validate(value)
        except exceptions.FieldValidationError as e:
            raise exceptions.FieldValidationError(
                'Got wrong email value: {}'.format(value))

    def mock_data(self):
        name = ''.join(random.sample(string.lowercase, 5))
        domain = '{0}.com'.format(''.join(random.sample(string.lowercase, 3)))
        return '{0}@{1}'.format(name, domain)


class IPAddredssField(BaseField):
    INTERNAL_TYPE = six.string_types
    FIELD_TYPE_NAME = 'ip_address'
    SUPPORT_VERSIONS = [4, 6, 'all']

    def __init__(self, version='all', **kwargs):

        super(IPAddredssField, self).__init__(**kwargs)

    def _validate(self, value):
        return value

    def _validate_ipv4(self, value):
        pass

    def _validate_ipv6(self, value):
        pass

    def mock_data(self):
        return None


class EnumField(BaseField):
    INTERNAL_TYPE = (list, tuple)
    FIELD_TYPE_NAME = 'enum'

    def __init__(self, choices=None, **kwargs):
        if choices is None or len(choices) == 0:
            raise ValueError('choices cant be empty or None')
        self.choices = choices

        super(EnumField, self).__init__(**kwargs)

    def _validate(self, value):
        if value not in self.choices:
            raise exceptions.FieldValidationError(
                '{!r} not in the choices'.format(value))
        return value

    def mock_data(self):
        return random.choice(self.choices)


class DictField(BaseField):
    INTERNAL_TYPE = dict
    FIELD_TYPE_NAME = 'dict'

    def __init__(self, validator=None, **kwargs):
        """
        :param validator: Validator object
        """
        self.validator = validator
        super(DictField, self).__init__(**kwargs)

    def _validate(self, value):
        value = self._validate_type(value)

        if self.validator:
            v = self.validator(value)
            if v.is_valid():
                value = v.validated_data
            else:
                raise exceptions.FieldValidationError(v.errors)
        else:
            value = copy.deepcopy(value)
        return value

    def mock_data(self):
        if self.validator:
            return self.validator.mock_data()
        else:
            return {}


class ListField(BaseField):
    INTERNAL_TYPE = (list, tuple)
    FIELD_TYPE_NAME = 'list'

    def __init__(self, field=None, min_length=None, max_length=None, **kwargs):
        self.field = field

        self._check_value_range(min_length, max_length)
        self.min_length = min_length
        self.max_length = max_length

        super(ListField, self).__init__(**kwargs)

    def _validate(self, value):
        value = self._validate_type(value)
        if self.min_length is not None and len(value) < self.min_length:
            raise exceptions.FieldValidationError(
                'this list has too few elements, min length is {}'.format(self.min_length))

        if self.max_length is not None and len(value) > self.max_length:
            raise exceptions.FieldValidationError(
                'this list has too many elements, max length is {}'.format(self.max_length))

        if self.field:
            new_value = []
            for item in value:
                new_item = self.field.validate(item)
                new_value.append(new_item)
            value = new_value
        else:
            value = copy.deepcopy(value)
        return value

    def mock_data(self):
        min_ = self.min_length
        if min_ is None:
            min_ = 0
        max_ = self.max_length
        if max_ is None:
            max_ = 10
        length = random.choice(xrange(min_, max_))

        data = [None] * length
        if self.field:
            for i in xrange(length):
                data[i] = self.field.mock_data()
        return data


class TimestampField(IntegerField):
    FIELD_TYPE_NAME = 'timestamp'

    def __init__(self, **kwargs):
        super(TimestampField, self).__init__(
            min_value=0, max_value=2 ** 32 - 1, **kwargs)

    def _validate(self, value):
        try:
            return super(TimestampField, self)._validate(value)
        except exceptions.FieldValidationError as e:
            raise exceptions.FieldValidationError(
                'Got wrong timestamp: {}'.format(value))


class DatetimeField(BaseField):
    INTERNAL_TYPE = datetime.datetime
    FIELD_TYPE_NAME = 'datetime'
    DEFAULT_FORMAT = '%Y/%m/%d %H:%M:%S'

    def __init__(self, dt_format=None, tzinfo=None, **kwargs):
        if dt_format is None:
            dt_format = self.DEFAULT_FORMAT
        self.format = dt_format
        self.tzinfo = tzinfo
        kwargs.setdefault('strict', False)
        super(DatetimeField, self).__init__(**kwargs)

    def _convert_type(self, value):
        # override
        if isinstance(value, six.string_types):
            if value.isdigit():
                value = int(value)
                return self.INTERNAL_TYPE.fromtimestamp(value, tz=self.tzinfo)
            else:
                dt = self.INTERNAL_TYPE.strptime(value, self.format)
                if self.tzinfo:
                    dt = dt.astimezone(self.tzinfo)
                return dt
        elif isinstance(value, six.integer_types):
            return self.INTERNAL_TYPE.fromtimestamp(value, tz=self.tzinfo)
        else:
            raise ValueError()

    def _validate(self, value):
        value = self._validate_type(value)
        return copy.copy(value)

    def to_presentation(self, value):
        return value.strftime(self.format)

    def mock_data(self):
        return self.INTERNAL_TYPE.fromtimestamp(random.randint(0, 2 ** 32 - 1))


class DateField(BaseField):
    INTERNAL_TYPE = datetime.date
    FIELD_TYPE_NAME = 'date'
    DEFAULT_FORMAT = '%Y/%m/%d'

    def __init__(self, dt_format=None, **kwargs):
        if dt_format is None:
            dt_format = self.DEFAULT_FORMAT
        self.format = dt_format
        kwargs.setdefault('strict', False)
        super(DateField, self).__init__(**kwargs)

    def _convert_type(self, value):
        # override
        if isinstance(value, six.string_types):
            if value.isdigit():
                value = int(value)
                return self.INTERNAL_TYPE.fromtimestamp(value)
            else:
                dt = datetime.datetime.strptime(value, self.format)
                return dt.date()
        elif isinstance(value, six.integer_types):
            return self.INTERNAL_TYPE.fromtimestamp(value)
        else:
            raise ValueError()

    def _validate(self, value):
        value = self._validate_type(value)
        return copy.copy(value)

    def to_presentation(self, value):
        return value.strftime(self.format)

    def mock_data(self):
        return self.INTERNAL_TYPE.fromtimestamp(random.randint(0, 2 ** 32 - 1))
