# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six
import random
import string
import sys
import uuid
import re
import copy
import datetime
from collections import OrderedDict
from six.moves import urllib_parse as urlparse, range
from IPy import IP, MAX_IPV4_ADDRESS, MAX_IPV6_ADDRESS
from . import exceptions
from .utils import force_text


__all__ = [
    # Don't need to add field to here by hand,
    # BaseFieldMetaClass will auto add field to here.
]

FIELDS_NAME_MAP = {
    # Don't need to add field to here by hand,
    # BaseFieldMetaClass will auto add field to here.
}


def create_field(field_info):
    """
    Create a field by field info dict.
    """
    field_type = field_info.get('type')
    if field_type not in FIELDS_NAME_MAP:
        raise ValueError('not support this field: {}'.format(field_type))
    field_class = FIELDS_NAME_MAP.get(field_type)
    params = dict(field_info)
    params.pop('type')
    return field_class.from_dict(params)


class EmptyValue(object):
    """
    a data type replace None
    """

    def __init__(self):
        pass

    def __str__(self):
        return '__empty_value__'

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


EMPTY_VALUE = EmptyValue()


class BaseFieldMetaClass(type):

    def __new__(cls, name, bases, attrs):
        __all__.append(name)
        clazz = super(BaseFieldMetaClass, cls).__new__(cls, name, bases, attrs)
        field_name = attrs.get('FIELD_TYPE_NAME')
        if field_name is not None and field_name != 'object':
            FIELDS_NAME_MAP[field_name] = clazz
        return clazz


@six.add_metaclass(BaseFieldMetaClass)
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

    @classmethod
    def _get_all_params(cls):
        """
        Collect all PARAMS from this class and its parent class.
        """
        params = list(cls.PARAMS)
        bases = cls.__bases__
        for base in bases:
            if issubclass(base, BaseField):
                params.extend(base._get_all_params())
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
                        'type convertion({0} -> {1}) is failed: {2}'.format(type(value).__name__, self.FIELD_TYPE_NAME, str(e)))
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
        params = self._get_all_params()
        for name in params:
            if hasattr(self, name):
                value = getattr(self, name)
                # 处理特殊值
                if value is EMPTY_VALUE:
                    value = '__empty__'
                d[name] = value
        return d

    @classmethod
    def from_dict(cls, params):
        """
        Create a field from params.
        sub-class can override this method.
        """
        if params.get('default') == '__empty__':
            params['default'] = EMPTY_VALUE
        return cls(**params)

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
    PARAMS = ['min_length', 'max_length', 'regex']

    def __init__(self, min_length=0, max_length=None, regex=None, **kwargs):
        if min_length < 0:
            min_length = 0
        self._check_value_range(min_length, max_length)
        self.min_length = min_length
        self.max_length = max_length

        if isinstance(regex, six.string_types):
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
            [random.choice(string.ascii_letters + string.digits) for _ in range(size)])
        random_str = self.to_internal(random_str)
        return random_str


class NumberField(BaseField):
    if six.PY2:
        INTERNAL_TYPE = (int, long, float)
    else:
        INTERNAL_TYPE = (int, float)
    FIELD_TYPE_NAME = 'number'
    PARAMS = ['min_value', 'max_value']

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
    PARAMS = []

    def mock_data(self):
        d = super(IntegerField, self).mock_data()
        return int(d)


class FloatField(NumberField):
    INTERNAL_TYPE = float
    FIELD_TYPE_NAME = 'float'
    PARAMS = []


class BoolField(BaseField):
    INTERNAL_TYPE = bool
    FIELD_TYPE_NAME = 'bool'
    PARAMS = []

    def mock_data(self):
        return random.choice([True, False])


class UUIDField(BaseField):
    INTERNAL_TYPE = uuid.UUID
    FIELD_TYPE_NAME = 'UUID'
    PARAMS = ['format']
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
    PARAMS = []
    REGEX = r'[\da-fA-F]{32}'

    def __init__(self, **kwargs):
        kwargs['strict'] = True
        super(MD5Field, self).__init__(min_length=32,
                                       max_length=32,
                                       regex=self.REGEX,
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
    PARAMS = ['version']

    def __init__(self, version=256, **kwargs):
        if version not in self.SUPPORT_VERSION:
            raise ValueError('{0} not support, support versions are: {1}'.format(
                version, self.SUPPORT_VERSION))
        if version == 1:
            length = 40
        else:
            length = int(version / 8 * 2)
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
    PARAMS = []

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
        name = ''.join(random.sample(string.ascii_lowercase, 5))
        domain = '{0}.com'.format(''.join(random.sample(string.ascii_lowercase, 3)))
        return '{0}@{1}'.format(name, domain)


class IPAddressField(BaseField):
    INTERNAL_TYPE = IP
    FIELD_TYPE_NAME = 'ip_address'
    PARAMS = ['version']
    SUPPORT_VERSIONS = ['ipv4', 'ipv6', 'both']

    def __init__(self, version='both', **kwargs):
        if version not in self.SUPPORT_VERSIONS:
            raise ValueError('{} version is not supported'.format(version))
        self.version = version

        kwargs.setdefault('strict', False)
        super(IPAddressField, self).__init__(**kwargs)

    def _validate(self, value):
        try:
            value = IP(value)
        except ValueError as e:
            raise exceptions.FieldValidationError(str(e))
        if self.version == 'ipv4' and value.version() != 4:
            raise exceptions.FieldValidationError(
                'expected an ipv4 address, got {}'.format(value.strNormal()))
        if self.version == 'ipv6' and value.version() != 6:
            raise exceptions.FieldValidationError(
                'expected an ipv6 address, got {}'.format(value.strNormal()))
        return value

    def to_presentation(self, value):
        return value.strNormal()

    def mock_data(self):
        v = self.version
        if v == 'both':
            v = random.choice(['ipv4', 'ipv6'])

        if v == 'ipv4':
            ip = random.randint(0, MAX_IPV4_ADDRESS)
            return IP(ip)
        else:
            ip = random.randint(0, MAX_IPV6_ADDRESS)
            return IP(ip)


class URLField(StringField):
    FIELD_TYPE_NAME = 'url'
    PARAMS = []
    SCHEMAS = ('http', 'http')

    def __init__(self, **kwargs):
        kwargs['strict'] = True
        super(URLField, self).__init__(min_length=0, **kwargs)

    def _validate(self, value):
        value = self._validate_type(value)
        url = urlparse.urlparse(value)
        if url.scheme not in self.SCHEMAS:
            raise exceptions.FieldValidationError('schema is lost')
        if url.hostname == '':
            raise exceptions.FieldValidationError('hostname is lost')
        return url.geturl()

    def mock_data(self):
        return 'http://www.example.com/media/image/demo.jpg'


class EnumField(BaseField):
    INTERNAL_TYPE = object
    FIELD_TYPE_NAME = 'enum'
    PARAMS = ['choices']

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
    PARAMS = ['validator']

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
    
    def to_dict(self):
        d = super(DictField, self).to_dict()
        if d['validator'] is not None:
            d['validator'] = d['validator'].to_dict()
        return d

    def mock_data(self):
        if self.validator:
            return self.validator.mock_data()
        else:
            return {}


class ListField(BaseField):
    INTERNAL_TYPE = (list, tuple)
    FIELD_TYPE_NAME = 'list'
    PARAMS = ['field', 'min_length', 'max_length']

    def __init__(self, field=None, min_length=0, max_length=None, **kwargs):
        if field is not None and not isinstance(field, BaseField):
            raise ValueError(
                'field param expect a instance of BaseField, but got {!r}'.format(field))
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

    def to_dict(self):
        d = super(ListField, self).to_dict()
        if d['field'] is not None:
            d['field'] = d['field'].to_dict()
        return d

    @classmethod
    def from_dict(cls, params):
        if 'field' in params and isinstance(params['field'], dict):
            params['field'] = create_field(params['field'])
        return super(ListField, cls).from_dict(params)

    def mock_data(self):
        min_ = self.min_length
        if min_ is None:
            min_ = 0
        max_ = self.max_length
        if max_ is None:
            max_ = 10
        length = random.choice(range(min_, max_))

        data = [None] * length
        if self.field:
            for i in range(length):
                data[i] = self.field.mock_data()
        return data


class TimestampField(IntegerField):
    FIELD_TYPE_NAME = 'timestamp'
    PARAMS = []

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
    PARAMS = ['dt_format', 'tzinfo']
    DEFAULT_FORMAT = '%Y/%m/%d %H:%M:%S'

    def __init__(self, dt_format=None, tzinfo=None, **kwargs):
        if dt_format is None:
            dt_format = self.DEFAULT_FORMAT
        self.dt_format = dt_format
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
                dt = self.INTERNAL_TYPE.strptime(value, self.dt_format)
                if self.tzinfo:
                    dt = dt.replace(tzinfo=self.tzinfo)
                return dt
        elif isinstance(value, six.integer_types):
            return self.INTERNAL_TYPE.fromtimestamp(value, tz=self.tzinfo)
        else:
            raise ValueError('Got wrong datetime value: {}'.format(value))

    def _validate(self, value):
        value = self._validate_type(value)
        return copy.copy(value)

    def to_presentation(self, value):
        return value.strftime(self.dt_format)

    def to_dict(self):
        d = super(DatetimeField, self).to_dict()
        if d['tzinfo'] is not None:
            d['tzinfo'] = force_text(d['tzinfo'])
        return d

    @classmethod
    def from_dict(cls, params):
        if 'tzinfo' in params and isinstance(params['tzinfo'], six.string_types):
            try:
                import pytz
            except ImportError as e:
                raise ValueError('Cant create DatetimeField instance with tzinfo {}, please install pytz and try again'.format(params['tzinfo']))
            params['tzinfo'] = pytz.timezone(params['tzinfo'])
        return super(DatetimeField, cls).from_dict(params)

    def mock_data(self):
        return self.INTERNAL_TYPE.fromtimestamp(random.randint(0, 2 ** 32 - 1))


class DateField(BaseField):
    INTERNAL_TYPE = datetime.date
    FIELD_TYPE_NAME = 'date'
    PARAMS = ['dt_format']
    DEFAULT_FORMAT = '%Y/%m/%d'

    def __init__(self, dt_format=None, **kwargs):
        if dt_format is None:
            dt_format = self.DEFAULT_FORMAT
        self.dt_format = dt_format
        kwargs.setdefault('strict', False)
        super(DateField, self).__init__(**kwargs)

    def _convert_type(self, value):
        # override
        if isinstance(value, six.string_types):
            if value.isdigit():
                value = int(value)
                return self.INTERNAL_TYPE.fromtimestamp(value)
            else:
                dt = datetime.datetime.strptime(value, self.dt_format)
                return dt.date()
        elif isinstance(value, six.integer_types):
            return self.INTERNAL_TYPE.fromtimestamp(value)
        else:
            raise ValueError()

    def _validate(self, value):
        value = self._validate_type(value)
        return copy.copy(value)

    def to_presentation(self, value):
        return value.strftime(self.dt_format)

    def mock_data(self):
        return self.INTERNAL_TYPE.fromtimestamp(random.randint(0, 2 ** 32 - 1))
