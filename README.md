# python-validator

python-validator 是一个类似于 Django ORM 的数据校验库，对于熟悉 Django 的开发人员非常友好。

本篇文档 将会介绍 python-validator 的各种基础用法和高级功能。

- [在线文档]()

- [更新记录]()

## 使用场景

python-validator 适用与任何需要进行数据校验的应用，比较常见的是 Web 后端校验前端的输入数据。

## 特性

- 支持 python2 和 python3。

- 使用类描述数据结构，数据字段一目了然。另外也支持使用字典定义数据结构。

- 可以自动生成用于测试的 mocking data。

- 可以打印出清晰的数据结构。

- 易于扩展。


## 安装

`pip install python-validator`


## 快速入门

假设现在正在开发一个上传用户信息的接口`POST /api/user/`，用户信息如下：

|字段|类型|描述|
|--|--|--|
|name|String| 必选|
|age|integer| 可选，默认20|
|sex|String, 'f'表示女, 'm'表示男|可选, 默认 None|

原始的、枯燥无味的、重复性劳动的数据校验代码可能是下面这样：

```python
def user(request):
    # data = json.loads(request.body)
    data = {
        'age': '24f',
        'sex': 'f'
    }
    name = data.get('name')
    age = data.get('age', 20)
    sex = dage.get('sex')

    if name is None or len(name) == 0:
        return Response('必须提供 name', status=400)
    
    try:
        age = int(age)
    except ValueError as e:
        return Response('age 格式错误', status=400)
    
    if sex is not None and sex not in ('f', 'm'):
        return Response('sex 格式错误', status=400)
    
    user_info = {
        'name': name,
        'age': age,
        'sex': sex,
    }
    ...
```

上面这段代码总的来说有几个问题：

- 枯燥无味和重复性代码，不断的取出数据，检查字段是否缺失，类型是否合法等等。

- 从数据校验的代码无法轻易看出用户信息的数据结构，即字段是什么类型的，是否可选，默认值是什么。

**使用 python-validator 校验数据**

首先定义一个 UserInfoValidator类

```python
# validators.py
from validator import Validator, StringField, IntegerField, EnumField

class UserInfoValidator(Validator):
    name = StringField(max_length=50, required=True)
    age = IntegerField(min_value=1, max_value=120, default=20)
    sex = EnumField(choices=['f', 'm'])
```

接下来使用`UserInfoValidator`进行数据校验，

```python
from .validators import UserInfoValidator

def user(request):
    # data = json.loads(request.body)
    data = {
        'age': '24',
        'sex': 'f'
    }
    v = UserInfoValidator(data)
    if not v.is_valid():
        return Response({'msg': v.str_errors, 'code': 400}, status=400)
    
    user_info = v.validated_data
    ...
```

`v.str_errors` 是一个字段名-错误信息的 dict，例如：

```python
{'age': 'got a wrong type: str, expect integer', 'name': 'Field is required'}
```

错误信息解释：

- `age` 等于 "24"，不是合法的 `int` 类型。

- `name`是必须提供的，且没有指定默认值。


v.validated_data 是校验后合法的数据，例如：

```json
{'age': 24, 'name': u'Michael', 'sex': 'f'}
```

下面是一些错误数据的例子：

```python
data:  {'age': 24, 'name': 'abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabc', 'sex': 'f'}
is_valid: False
errors: {'name': 'string is too long, max-lenght is 50'}
validated_data: None
```

```python
data:  {'age': 24, 'name': 'Michael', 'sex': 'c'}
is_valid: False
errors: {'sex': "'c' not in the choices"}
validated_data: None
```

细心的同学可能发现了 `IntegerField` 不接受“数字字符串”，上面的例子中 `age` 是一个 `IntegerField`，形如`'24'`这样的值是非法的。在某些情况下，你可能希望 `IntegerField` 不要这么严格，`'24'`这样的值也是可以接受的，那么可以把`strict`选项设为 `False`，如：`age = IntegerField(min_value=1, max_value=120, default=20, strict=False)`。当`strict`选项为 `False`时，python-validator 会尝试进行类型转换，假如转换失败则会报错。



