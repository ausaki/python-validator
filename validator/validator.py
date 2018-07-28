# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six
from . import exceptions
from .fields import BaseField, EMPTY_VALUE, create_field, DictField
from .utils import force_str

class ValidatorMetaClass(type):

    def __new__(cls, cls_name, bases, attrs):
        fields_map = dict()
        parent_fields_map = dict()
        for parent in bases:
            if hasattr(parent, '_FIELDS_MAP'):
                parent_fields_map.update(parent._FIELDS_MAP)

        for name, value in six.iteritems(attrs):
            if isinstance(value, BaseField):
                fields_map[name] = value

        for name in fields_map:
            attrs.pop(name, None)

        parent_fields_map.update(fields_map)

        attrs['_FIELDS_MAP'] = parent_fields_map

        return super(ValidatorMetaClass, cls).__new__(cls, cls_name, bases, attrs)


@six.add_metaclass(ValidatorMetaClass)
class Validator(object):
    """ a data validator like Django ORM
    """

    def __init__(self, raw_data):
        """
        :param raw_data: unvalidate data
        """
        assert isinstance(raw_data, dict)
        self.raw_data = raw_data
        self.validated_data = None
        self.errors = {}

    def _validate(self):
        data = {}
        for name, field in six.iteritems(self._FIELDS_MAP):
            value = self.raw_data.get(name, field.get_default())
            if value is EMPTY_VALUE and field.is_required():
                self.errors[name] = exceptions.FieldRequiredError()
                continue

            # dont need to validate EMPTY_VALUE or None
            if value is EMPTY_VALUE or None:
                data[name] = None
                continue

            try:
                validated_value = field.validate(value)
                internal_value = field.to_internal(validated_value)
                field_validator = getattr(
                    self, 'validate_{}'.format(name), None)
                if field_validator and callable(field_validator):
                    field_validator(internal_value)
                data[name] = internal_value
            except exceptions.FieldValidationError as e:
                self.errors[name] = e

        if self.errors:
            return
        try:
            data = self.validate(data)
        except exceptions.ValidationError as e:
            self.errors['__data_error__'] = [e]

        if not self.errors:
            self.validated_data = data

    def is_valid(self, raise_error=False):
        self._validate()
        if raise_error and self.errors:
            raise exceptions.ValidationError(self.errors)
        return False if self.errors else True

    def validate(self, data):
        """
        model-level validate.
        sub-class can override this method to validate data, return modified data
        """
        return data

    @property
    def str_errors(self):
        errors = dict()
        for name, error in six.iteritems(self.errors):
            errors[name] = error.get_detail()
        return errors

    @classmethod
    def to_dict(cls):
        """
        format Validator to dict 
        """
        d = dict()
        for name, field in six.iteritems(cls._FIELDS_MAP):
            field_info = field.to_dict()
            d[name] = field_info
        return d

    @classmethod
    def mock_data(cls):
        """
        return random mocking data. 
        mocking data will be valid in most case, but it maybe can't pass from your own `validate` method or `validator`
        """
        mocking_data = {}
        for name, field in six.iteritems(cls._FIELDS_MAP):
            mocking_data[name] = field.mock_data()
        return mocking_data

    def _format(self):
        fields = []
        for name, field in six.iteritems(self._FIELDS_MAP):
            fields.append('{0}:{1}'.format(name, field.FIELD_TYPE_NAME))
        fields = ','.join(fields)
        if len(fields) > 103:
            fields = fields[:100]
        return '<{0}: {1}>'.format(self.__class__.__name__, fields)

    def __str__(self):
        return self._format()

    def __repr__(self):
        return self._format()


def create_validator(data_struct_dict, name=None):
    """
    create a Validator instance from data_struct_dict

    :param data_struct_dict: a dict describe validator's fields, like the dict `to_dict()` method returned.
    :param name: name of Validator class 

    :return: Validator instance
    """

    if name is None:
        name = 'FromDictValidator'
    attrs = {}
    for field_name, field_info in six.iteritems(data_struct_dict):
        field_type = field_info['type']
        if field_type == DictField.FIELD_TYPE_NAME and isinstance(field_info.get('validator'), dict):
            field_info['validator'] = create_validator(field_info['validator'])
        attrs[field_name] = create_field(field_info)
    name = force_str(name)
    return type(name, (Validator, ), attrs)
