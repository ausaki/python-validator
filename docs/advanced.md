# 进阶

python-validator 主要包含 `Validator` 和 `XXXField` 两部分，`Validator` 类似于 Django 中的 Model，用于描述数据结构，其中的 `XXXField` 描述了字段的类型和约束，`XXXField` 负责校验对应的数据。

---

## 定义 Validator

直接继承 `Validator` 类并列出包含的字段

```python
from validator import Validator, StringField, IntegerField, EnumField

class UserInfoValidator(Validator):
    name = StringField(max_length=50, required=True)
    age = IntegerField(min_value=1, max_value=120, default=20)
    sex = EnumField(choices=['f', 'm'])
```

上面的代码定义了一个校验用户信息的 `Validator`:

- name 是一个字符串，最大长度为 50 个字节，并且必须提供不能缺失。注意这里的长度指的是字节，而不是字符。

- age 是一个整形，最小值 1，最大值 120，非必须，默认值 20

- sex 是一个枚举类型，可选值：['f', 'm']，非必须。

当 `required` 为 `True` 时，该字段必须提供，除非显式指定 `default` 值。如果 `required` 为 `True` 且没有指定 `default` 值，当字段不存在时将会发生异常 `FieldValidationError`。以上面的 `UserInfoValidator` 为例，下面的数据将会发生异常：

```python
data = {
    # 缺少 name 字段
    'age': 20,
    'sex': 'f'
}
```
python-validator 还支持 [通过数据结构字典创建 Validator](#validator_1)。

关于字段参数请参考 [字段 API](fields.md)。

---

## 校验数据

使用 `is_valid()` 校验数据，数据合法该方法返回 `True`，否则返回 `False`。

```python
data = {
    'name:'Bob',
    'age': 30,
    'sex': 'm'
}
v = UserInfoValidator(data)
print(v.is_valid()) #  校验数据
print(v.validated_data) # 获取校验过的数据
```

如果数据不合法，那么 `v.validated_data` 是 None。

`is_valid()` 其实还接受一个可选的参数 `raise_error`，该参数默认为 `False`，
如果 `raise_error` 为 `True`，那么当数据非法时，`is_valid()` 会触发异常 `ValidationError`，而不是返回 `False`。

---

## 错误信息

错误信息保存在实例属性 `errors` 中，`errors` 是一个字典，包含了每个错误字段的错误信息，例如：

```python
# data
{
    'age': '24',
    'sex': 'f'
}
# v.errors
{
    'age': <FieldValidationError: got a wrong type: str, expect integer>,
    'name': <FieldRequiredError: Field is required>
}
```

`str_errors` 属性是格式化之后的错误信息，例如：

```python
{
    'age': 'got a wrong type: str, expect integer',
    'name': 'Field is required'
}
```

---

## 自定义字段级的校验方法

`Validator` 在校验数据时会自动调用形如 `validate_xxx` 的方法校验字段数据。
`validate_xxx` 方法接受一个参数 `value`（已经校验过的值），无需返回任何值。如果数据非法，触发 `FieldValidationError` 异常即可。

> 将 xxx 替换为字段名

代码示例：

```python
from validator import Validator, StringField, IntegerField, EnumField, FieldValidationError

class UserInfoValidator(Validator):
    name = StringField(max_length=50, required=True)
    age = IntegerField(min_value=1, max_value=120, default=20)
    sex = EnumField(choices=['f', 'm'])

    def validate_name(self, value):
        if value == 'foo':
            raise FieldValidationError('"foo" is invalid')

```

** 注意：不建议在 `validate_xxx` 方法中修改 `value`**

---

## 自定义全局的校验方法

当校验完所有字段的数据后，`Validator` 会调用 `validate` 方法校验全局数据，此时的全局数据是一个已经校验过的 dict。默认的 `validate` 方法直接返回数据，你可以覆盖它以实现自己的校验逻辑。

代码示例：

```python
from validator import Validator, StringField, IntegerField, EnumField, ValidationError

class UserInfoValidator(Validator):
    name = StringField(max_length=50, required=True)
    age = IntegerField(min_value=1, max_value=120, default=20)
    sex = EnumField(choices=['f', 'm'])

    def validate(self, data):
        if data['name'] == 'Bob' and data['age'] > 60:
            raise ValidationError('Bob is too old, he is younger than 60 age')
        # 你也可以在这里修改 data 的数据
        # data['foo'] = 'bar'
        return data
```

---

## 生成测试数据

类方法 `mock_data()` 方法可以生成测试数据，该数据不保证完全通过校验，特别是通过 “自定义字段级的校验方法” 和 “自定义全局的校验方法” 的校验。

代码示例：

```python
data = UserInfoValidator.mock_data()
print(data) # {'age': 74, 'name': u'R7fuZaWOCPUVeYSQqaUvI', 'sex': 'f'}
```

---

## to_dict

类方法 `to_dict(cls)` 返回一个描述数据结构的 dict，例如：

```python
{
    "age": {
        "required": false,
        "default": 20,
        "max_value": 120,
        "min_value": 1,
        "strict": true,
        "validators": [],
        "type": "integer"
    },
    "name": {
        "regex": null,
        "min_length": 0,
        "max_length": 50,
        "strict": true,
        "default": "__empty__",
        "validators": [],
        "required": true,
        "type": "string"
    },
    "sex": {
        "default": "__empty__",
        "required": false,
        "choices": [
            "f",
            "m"
        ],
        "strict": true,
        "validators": [],
        "type": "enum"
    }
}
```

---

## 数据结构字典

数据结构字典的 key 是字段名称，value 是描述字段的类型和初始化参数的字典。

以上面 `to_dict` 返回的字典为例，`age`， `name`，和 `sex` 都是字段名称，其对应的值包含了字段类型和初始化参数。

`type` 表示字符串形式的字段类型，每个字段的字符串形式的字段类型保存在 `FIELD_TYPE_NAME` 属性中。剩余的都是字段的初始化参数。

假如 `default`等于 `EMPTY_VALUE`，为了方便则使用'__empty__'表示。

### 特殊字段

- ListField

    

- DictField

- DatetimeField

---

## 通过数据结构字典创建 Validator

`create_validator(data_struct_dict, name=None)`

根据 `data_struct_dict` 创建一个 Validator 实例。`data_struct_dict` 是一个描述数据结构的字典，类似于 `to_dict` 返回的字典。

示例：

```python
data = {
    'name': {
        'type': 'string',
        'min_length': 10,
        'max_length': 20,
    }
}
V = create_validator(data)
```