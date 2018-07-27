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