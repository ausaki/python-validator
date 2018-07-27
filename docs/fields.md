# 字段 API

下面将要介绍 python-validator 中所有的字段，


## BaseField

所有字段的父类。

- `__init__(self, strict=True, default=EMPTY_VALUE, validators=None, required=False, **kwargs)`

    - strict

        bool 类型，是否采用严格类型校验。当 `strict = True` 时，值必须是该字段类型的实例，即 `isinstance(value, INTERNAL_TYPE)`，否则发生异常 `FieldValidationError('got a wrong type: {0}, expect {1}')`。 当 `strict = False` 时，如果值不是字段类型的实例，会尝试进行类型转换，假如转换失败发生异常 `FieldValidationError('type convertion is failed: {0} -> {1}')`

    - default

        字段的默认值。`default` 默认为 `EMPTY_VALUE`， `EMPTY_VALUE` 是 python-validator 内部使用的一个空值，以区别 None。当待校验数据中缺失该字段时，使用 `default` 。 python-validator 会对 `default` 进行校验（除非 `default` 等于 `EMPTY_VALUE` 或者 `None`），所以请提供合法的 `default`。

    - required

        bool 类型，字段是否是必须的。如果该字段是必须的且没有指定默认值，会导致异常 `FieldRequiredError`。

    - validators

        列表类型，提供一组额外的校验器。validator 可以是函数或者其它可调用的对象，validator 接受一个参数，即字段值。函数的返回值无效，因此无法实现级联校验的效果（`value | validate(value) | validate(value)`）。不要在函数中修改字段值。

    - kwargs

        目前未使用。

- 类属性

    - INTERNAL_TYPE

        字段内部类型。可以是单个类型或者类型列表，例如 `StringField` 的 `INTERNAL_TYPE` 等于 `str`（in Python2）或者 `(str, unicode)`（in python3）

    - FIELD_TYPE_NAME

        字段类型名字。字符串形式的类型名字，主要是为了可读性和方便显示。

    - PARAMS

        参数名称列表。`PARAMS` 包含所有初始化方法所需的参数名称。例如 `BaseField` 的 `PARAMS` 等于 `['strict', 'default', 'validators', 'required']`

- 方法

    - `validate(self, value)`

        暴露给外部调用的校验数据方法，该方法首先调用 `_validate()` 校验数据，接着遍历 `validators` 校验数据，最后返回校验后的值。

    - `_validate(self, value)`

        私有校验数据方法，校验成功应该返回合法值，失败则触发异常 `FieldValidationError`。子类应该覆盖该方法实现自己的校验逻辑。如果 `value` 是可变类型的数据，建议拷贝一份 `value`，防止修改数据影响到原始数据。

    - `_validate_type(self, value)`

        校验数据类型。`_validate` 可以调用该方法校验数据类型。校验类型的逻辑如下：

        - 如果 `value` 不是 `INTERNAL_TYPE` 的实例，

            - 如果 `strict` 为 `True`，则触发异常 `FieldValidationError`。

            - 如果 `strict` 为 `False`，则尝试进行类型转换。转换成功返回转换后的值，转换失败触发 `FieldValidationError`。

        - 如果 `value` 是 `INTERNAL_TYPE` 的实例，则直接返回 `value`

    - `_convert_type(self, value)`

        转换数据类型，返回转换后的值。

    - `is_required(self)`

        该字段是否必须。

    - `get_default(self)`

        返回默认值。

    - `to_presentation(self, value)`

        将 `value` 转换为字符串形式，`value` 必须是经过校验合法的值。

    - `to_internal(self, value)`

        将 `value` 转换为内部形式，`value` 必须是经过校验合法的值。一般直接返回 `value`。

    - `to_dict(self)`

        将字段转换为字典形式，字典描述了该字段的类型和初始化参数。

    - `mock_data(self)`

        返回可用于测试的随机值。


## StringField

字符串字段，继承自 `BaseField`。

- `__init__(self, min_length=0, max_length=None, regex=None, **kwargs)`

    - min_length

        最小长度，以字节为单位。默认为 0，即允许空字符串。

    - max_length

        最大长度，以字节为单位。默认为 None，表示不限制最大长度。

    - regex

        正则表达式，测试字符串是否匹配。使用 `re.match` 进行匹配。`regex` 可以是字符串或者经过 `re.compile` 的 `_sre.SRE_Pattern` 对象。

    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - INTERNAL_TYPE

        in Python2: (str, unicode)

        in Python3: str

    - FIELD_TYPE_NAME

        'string'

    - PARAMS

        ['min_length', 'max_length', 'regex']

- 方法

    - `mock_data(self)`

        返回随机生成的一段字符串。字符串长度是一个随机值，介于 `min_length` 和 `max_length` 之间，如果 `max_length` 等于 `None`，则 `max_length = min_length + 100`。

## NumberField

普通数字字段，继承自 `BaseField`。

- `__init__(self, min_value=None, max_value=None, **kwargs)`

    - min_value

        最小值。默认为 None，即不限制最小值。

    - max_value

        最大值。默认为 None，即不限制最大值。

    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - INTERNAL_TYPE

        in Python2: (int, long, float)

        in Python3: (int, float)

    - FIELD_TYPE_NAME

        'number'

    - PARAMS

        ['min_value', 'max_value']

- 方法

    - `mock_data(self)`

        返回随机生成的一个数字。数字介于 `min_value` 和 `max_value` 之间，如果 `min_value` 等于 `None`，则 `min_value = 0`，如果 `max_value` 等于 `None`，则 `max_value = min_value + 1000`。


## IntegerField

整数字段，继承自 `NumberField`。


- 类属性

    - INTERNAL_TYPE

        in Python2: (int, long)

        in Python3: int

    - FIELD_TYPE_NAME

        'int'


## FloatField

浮点数字段，继承自 `NumberField`。

- 类属性

    - INTERNAL_TYPE

        float

    - FIELD_TYPE_NAME

        'float'

    - PARAMS

        []


## BoolField

BoolField，继承自 `BaseField`。

- 类属性

    - INTERNAL_TYPE

        bool

    - FIELD_TYPE_NAME

        'bool'

    - PARAMS

        []

- 方法

    - `mock_data(self)`

        返回 True 或 False


## UUIDField

UUID 字段，继承自 `BaseField`。

当 `strict` 为 `True` 时，值必须是 `uuid.UUID` 类型的。`strict` 为 `False` 时，值可以是 `uuid.UUID` 类型，也可以是形如'41e40df1-ef12-46d2-9290-4d3d9dbfe24f'，'41e40df1ef1246d292904d3d9dbfe24f'的字符串形式的值。

校验通过后返回一个 `uuid.UUID` 实例。


- `__init__(self, format='hex', **kwargs)`

    - format

        格式化类型，`to_presentation` 会用到。支持的 format 有：hex，str，int，bytes，bytes_le。

    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - INTERNAL_TYPE

       uuid.UUID

    - FIELD_TYPE_NAME

        'UUID'

    - PARAMS

        ['format']

- 方法

    - `mock_data(self)`

        返回由 `uuid.uuid4()` 随机生成的 `uuid.UUID` 实例。


## MD5Field

MD5 字段，继承自 `StringField`。

合法值为 32 字节的十六进制形式的字符串。

校验通过后返回一个原始字符串。


- `__init__(self, **kwargs)`
    覆盖父类初始化方法，`strict` 为 `True`，`min_length` 和 `max_length` 都等于 32。

    - kwargs

        其它参数，例如 `StringField`  或 `BaseField` 所需的参数。

- 类属性

    - FIELD_TYPE_NAME

        'md5'

    - PARAMS

        []

- 方法

    - `mock_data(self)`

        返回随机生成的一段 md5 字符串。


## SHAField

SHA 字段，继承自 `StringField`。

合法值为 N 字节的十六进制形式的字符串。

校验通过后返回一个原始字符串。

- `__init__(self, version=256, **kwargs)`

    覆盖父类初始化方法，`strict` 为 `True`，`min_length` 和 `max_length` 都等于对应 SHA 版本的长度，例如 SHA1 的 `min_length` 和 `max_length` 都等于 40。

    - version

        SHA 版本，支持的版本有：[1, 224, 256, 384, 512]

    - kwargs

        其它参数，例如 `StringField`  或 `BaseField` 所需的参数。

- 类属性

    - FIELD_TYPE_NAME

        'sha'

    - PARAMS

        []

- 方法

    - `mock_data(self)`

        返回随机生成的一段 sha 字符串。


## EmailField

Email 字段，继承自 `StringField`。

合法值为符合 email 格式的字符串。

校验通过后返回原始字符串。

- `__init__(self, **kwargs)`

    覆盖父类初始化方法，`strict` 强制设为 `True`。

    用于验证的正则表达式为:

    `r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'`

    - kwargs

        其它参数，例如 `StringField` 或 `BaseField` 所需的参数。

- 类属性

    - FIELD_TYPE_NAME

        'email'

    - PARAMS

        [ ]

- 方法

    - `mock_data(self)`

        返回随机生成的 email 字符串。

--------

## IPAddressField

IP 地址字段，继承自 `BaseField`。

支持 `IPV4 和 ` `IPV6`，数据的校验依赖于 `IPy` 库。

如果 `strict` 为 True，值必须是 `IPy.IP` 的实例。如果 `strict` 为 `False`，值 既可以是 `IPy.IP` 的实例，
也可以是任何 `IPy.IP` 支持的格式，例如：'127.0.0.1', '::1234:1234', '7f000001'，具体请参考 [IPy](https://github.com/autocracy/python-ipy)。

校验通过后返回 `IPy.IP` 实例。


- `__init__(self, version='both', **kwargs)`

    - version

        指定版本，支持的版本有：['ipv4', 'ipv6', 'both']

    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - INTERNAL_TYPE

        IPy.IP

    - FIELD_TYPE_NAME

        'ip_address'

    - PARAMS

        ['version']

- 方法

    - `mock_data(self)`

        返回随机生成的一个 IP 地址。


## URLField

字符串字段，继承自 `StringField`。

合法值为 `urlparse.urlparse` 能够正确解析且包含 `scheme` 和 `hostname` 的字符串，`scheme` 必须是'http'，'https'其中之一。

校验通过后返回原始字符串。


- `__init__(self, **kwargs)`

    覆盖父类初始化方法，`strict` 强制设为 `True`。

    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - FIELD_TYPE_NAME

        'url'

    - PARAMS

        [ ]

- 方法

    - `mock_data(self)`

        返回随机生成的 url。


## EnumField

枚举字段，继承自 `BaseField`。

合法值必须是 `choices` 其中一员。

校验通过后返回原始值。

`EnumField` 不验证数据类型，所以 `INTERNAL_TYPE` 等于 `object`。只要值在 `choices` 中就行了。


- `__init__(self, choices=None, **kwargs)`

    - choices

        可选值列表。

    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - INTERNAL_TYPE

       object

    - FIELD_TYPE_NAME

        'enum'

    - PARAMS

        ['choices']

- 方法

    - `mock_data(self)`

        返回随机从 choices 中挑选的值。

## DictField

字典字段，继承自 `BaseField`。

合法值必须是通过 `validator` 校验的 `dict`。

校验通过后返回原始值的拷贝。

- `__init__(self, validator=None, **kwargs)`

    - validator

        `Validator` 实例，用于验证字典内各个字段的数据。由于 `dict` 是一个 key-value 的复合数据结构，很难通过简单的规则去约束它，因此，最直接的方法就是定义一个 `Validator` 去校验 `dict`。

        如果 `validator` 等于 `None`，则任何 `dict` 都是合法的。

    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - INTERNAL_TYPE

        dict

    - FIELD_TYPE_NAME

        'dict'

    - PARAMS

        ['validator']

- 方法

    - `mock_data(self)`

         调用 `validator.mock_data()` 生成测试数据，如果 `validator` 等于 `None`，则返回空字典


## ListField

列表字段，继承自 `BaseField`。

合法值是一个通过 field 校验的列表（元组）。

校验通过后返回原始值的拷贝。

- `__init__(self, field=None, min_length=0, max_length=None, **kwargs)`

    - field

        列表元素的字段类型，必须是 BaseField 的实例。如果 field 等于 None，则不校验列表中的元素，意味着任何 list 都是合法的。

    - min_length

        最小长度。默认为 0，即允许空列表。

    - max_length

        最大长度。默认为 None，表示不限制最大长度。

    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - INTERNAL_TYPE

        (list, tuple)

    - FIELD_TYPE_NAME

        'list'

    - PARAMS

        ['field', 'min_length', 'max_length']

- 方法

    - `mock_data(self)`

        返回随机生成的一个列表，元素由 `field` 随机生成，长度在 `min_length` 和 `max_length` 之间。如果 `max_length` 等于 `None`，则假设等于 10。如果 `field` 等于 `None`，则列表元素都等于 `None`。


## TimestampField

时间戳字段，继承自 `IntegerField`。

合法值是一个无符号的 int32，值介于 `0` ~ `2 ** 32 - 1`。

校验通过后返回原始值。


- `__init__(self, **kwargs)`

    覆盖父类初始化方法，将 `min_value` 设为 `0`，`max_value` 设为 `2 ** 32 - 1`。

    - kwargs

        其它参数，例如 `IntegerField` 和 `BaseField` 所需的参数。

- 类属性

    - FIELD_TYPE_NAME

        'timestamp'

    - PARAMS

        [ ]

- 方法

    - `mock_data(self)`

        返回随机生成的时间戳。


## DatetimeField

日期时间字段，继承自 `BaseField`。

合法值可以是下面其中一个：

- `datatime.datetime` 的实例。

- 整数时间戳，如 1531815911。

- 字符串时间戳，如 '1531815911'。

- 符合 `dt_format` 的日期字符串。假设 `dt_format` 为 `'%Y/%m/%d %H:%M:%S'`，则合法的字符串为'2018/01/01 01:01:01'。

校验通过后返回一个 `datatime.datetime` 的实例。

- `__init__(self, dt_format=None, tzinfo=None, **kwargs)`

    - dt_format

        日期时间格式化字符串。如果 `dt_format` 等于 `None`，则将其设为默认值 `'%Y/%m/%d %H:%M:%S'`。

    - tzinfo

        时区信息，详情请参考[python datetime tzinfo](https://docs.python.org/3.7/library/datetime.html#datetime.tzinfo)。
        当校验通过后，会将日期的时区设为`tzinfo`。
        推荐使用 [pytz](https://github.com/newvem/pytz) 库获取各个国家地区的时区信息。


    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - INTERNAL_TYPE

       `datetime.datetime`

    - FIELD_TYPE_NAME

        'datetime'

    - PARAMS

        ['dt_format', 'tzinfo']

- 方法

    - `mock_data(self)`

        返回随机生成的日期时间。


## DateField

日期字段，继承自 `BaseField`。

合法值可以是下面其中一个：

- `datatime.date` 的实例。

- 整数时间戳，如 1531815911。

- 字符串时间戳，如 '1531815911'。

- 符合 `dt_format` 的日期字符串。假设 `dt_format` 为 `'%Y/%m/%d'`，则合法的字符串为'2018/01/01'。

校验通过后返回一个 `datatime.datetime` 的实例。


- `__init__(self, dt_format=None, **kwargs)`
   
    - dt_format

        日期格式化字符串。如果 `dt_format` 等于 `None`，则将其设为默认值 `'%Y/%m/%d'`。

    - kwargs

        其它参数，例如 `BaseField` 所需的参数。

- 类属性

    - INTERNAL_TYPE

        `datetime.date`

    - FIELD_TYPE_NAME

        'date'

    - PARAMS

        ['dt_format']

- 方法

    - `mock_data(self)`

        返回随机生成的日期。
