# 自定义字段

如果还没有看过 [字段 API](fields.md) 的话，建议先看完 [字段 API](fields.md) 再看本篇文档。

## 自定义字段步骤

- 定义字段类型，`INTERNAL_TYPE = YOUR_CUSTOM_FIELD_TYPE`

- 定义字段类型名称，`FIELD_TYPE_NAME = YOUR_CUSTOM_FIELD_TYPE_NAME`

- 定义 `PARAMS`，`PARAMS` 是一个参数名称列表，包含 `__init__` 方法所需的参数，但是不包含传递给父类的参数。如果 `__init__` 方法不需要任何参数，则将 `PARAMS` 设为空列表。

- 如有必要的话，覆盖 `__init__` 方法，记得调用父类的 `__init__` 方法。

- 实现`_validate(self, value)`方法，该方法用于验证数据，验证通过则返回数据，验证失败则抛出异常`FieldValidationError`。注意：如果原始数据是可变类型（如 list，dict），则最好返回原始数据的拷贝，以防止篡改数据。

    在`_validate`方法中，可以调用`_validate_type(self, value)` 验证参数类型。

- 实现`mock_data(self)`方法，返回用于测试的假数据。

## 例子

```python
from validator import Validator, BaseField, FieldValidationError
import random

class AgeField(BaseField):
    INTERNAL_TYPE = int
    FIELD_TYPE_NAME = 'age'
    PARAMS = []     # 由于没有覆盖__init__方法，所以 PARAMS 设为空列表

    def _validate(self, value):
        # 首先调用_validate_type(value) 校验数据类型
        value = self._validate_type(value)
        if value <= 0:
            raise FieldValidationError('年龄不能小于或等于 0')
        if value > 120:
            # 假设最大年龄是 120
            raise FieldValidationError('年龄不能超过 120')
        # 返回校验通过后的数据
        return value

    def mock_data(self):
        # 随机生成一个介于 1 ~ 120 的年龄
        return random.randint(1, 120)
```

如果想查看更多的例子，建议直接查看 python-validator 的源码。
