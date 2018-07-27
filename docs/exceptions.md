# 异常

## BaseValidationError

所有异常的基类。

- `__init__(self, detail=None, code=None)`

    - detail

        错误详情，可以是字符串或者 dict。

    - code

        错误代码，目前未使用到。

- 实例方法

    - `get_detail(self)`

        返回错误详情。

- 类属性

    - default_detail

        默认的错误详情。如果 `__init__` 的 `detail` 参数为 `None`，则将其设为 `default_detail`。

    - default_code

        默认的错误代码。如果 `__init__` 的 `code` 参数为 `None`，则将其设为 `default_code`。

---

## FieldRequiredError

继承自 BaseValidationError，当字段缺失时触发该异常。

```
default_detail = 'Field is required'
default_code = 'error'
```

---

## ValidationError

继承自 BaseValidationError，当 `Validator.validate()` 或者 `Validator.is_valid(raise_error=True)` 校验数据失败时触发该异常。

```
default_detail = 'Validation error'
default_code = 'error'
```

---

## FieldValidationError

继承自 BaseValidationError，当校验字段数据失败时触发该异常。

```
default_detail = 'field Validation error'
default_code = 'error'
```
