# 历史版本

## Version 0.0.8

- 修复 [#9](https://github.com/ausaki/python-validator/issues/9)

- 使用 poetry 替代之前的 pipenv.

- 删除一些代码.

## Version 0.0.7

- 添加 assert 语句的错误信息。

- 修复 URLField 的 scheme。

## Version 0.0.6

- 支持 i18n

- 修复 bug：BaseValidationError.**str** 在 python3 返回 bytes

## Version 0.0.5

- 修复 bug：当字段是可选的且数据中缺失该字段时，validated_data 将该字段值设为 None。正确的逻辑应该和原数据保持一致，validated_data 应该不存在该字段值。

## Version 0.0.4

- DatetimeField 的 tzinfo 参数支持时区名称字符串

- 放弃 python2.6

## Version 0.0.3

- 兼容 python3

- 支持通过数据字典创建 Validator（create_validator）

- 使用 TravisCI 测试代码

## Version 0.0.1

第一个发布版本.

- 支持以下字段:

  - StringField
  - NumberField
  - IntegerField
  - FloatField
  - BoolField
  - UUIDField
  - MD5Field
  - SHAField
  - EmailField
  - IPAddressField
  - URLField
  - EnumField
  - DictField
  - ListField
  - TimestampField
  - DatetimeField
  - DateField

- 支持自定义字段级字段验证

- 支持自定义全局数据验证
