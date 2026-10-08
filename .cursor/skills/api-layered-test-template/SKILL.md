---
name: api-layered-test-template
description: Add new API interfaces using a layered pattern for this webtools project. Use when creating or extending BM or H5 interfaces, writing single-interface tests, adding smoke tests, parameter coverage tests, or defining how API layer and tests layer should be separated.
---
# API Layered Test Template

适用于 `webtools` 项目中新增接口时的标准做法，目标是做到：
- `api` 层保持纯粹，便于场景复用
- `tests` 层负责单接口验证与参数覆盖
- 后续场景化编排可以直接复用接口层能力

## 一、分层原则

### 1. `api/app/*.py` 负责什么
只负责接口封装：
- 请求路径
- 请求参数组装
- 必要的自动补参
- 发请求并返回响应

不要在 `api` 层做这些事：
- 不写 pytest 用例
- 不做复杂断言
- 不做参数覆盖矩阵
- 不写场景编排逻辑

### 2. `tests/test_*.py` 负责什么
只负责测试验证：
- 单接口冒烟
- 关键参数覆盖
- 接口层自动补参能力验证
- 必要的异常场景验证

---

## 二、新增接口时的固定步骤

每新增一个接口，按下面顺序做：

1. 在对应 `api/app/*.py` 中增加接口方法
2. 先补 1 条固定参数的冒烟用例
3. 再补核心参数覆盖用例
4. 如果接口层有自动补参/自动查单号能力，再补 1 条封装能力验证用例

---

## 三、接口层模板

新增接口时，优先保持方法足够薄。

```python
def xxx_api(self, data: Optional[dict] = None):
    return self.post("/your/api/path", data=data or {})
```

如果存在必要自动补参，可以这样做：

```python
def _build_xxx_request_data(self, data: Optional[dict] = None):
    request_data = dict(data or {})
    request_data.setdefault("fieldA", "default_value")
    return request_data


def xxx_api(self, data: Optional[dict] = None):
    request_data = self._build_xxx_request_data(data)
    return self.post("/your/api/path", data=request_data)
```

### 约束
- 方法名直接表达业务含义
- 一个方法只封装一个接口
- 不在接口方法里写测试分支
- 自动补参只做“调用所必需”的部分

---

## 四、测试层模板

### 1. 冒烟用例模板
用于验证接口通路可用。

```python
def test_xxx_api_smoke(self, env):
    api = XxxApi(...)
    response = api.xxx_api(data={
        "key": "value"
    })

    assert response is not None, "响应为空"
    assert isinstance(response, dict), "响应应该是字典类型"
```

### 2. 参数覆盖模板
用于验证同一接口的核心业务分支。

```python
@pytest.mark.parametrize("scene", ["A", "B", "C"])
def test_xxx_api_different_scenes(self, env, scene):
    api = XxxApi(...)
    response = api.xxx_api(data={
        "scene": scene
    })

    assert response is not None, f"{scene} 响应为空"
    assert isinstance(response, dict), f"{scene} 响应应该是字典类型"
```

### 3. 封装能力验证模板
用于验证接口层自动补参是否生效。

```python
def test_xxx_api_auto_fill_field(self, env):
    api = XxxApi(...)
    response = api.xxx_api()

    assert response is not None, "自动补参场景响应为空"
```

---

## 五、推荐测试拆分

对每个新增接口，至少拆成两层：

### 第一层：固定参数冒烟
目标：
- 证明接口通
- 给后续场景编排提供稳定基础

### 第二层：关键参数覆盖
目标：
- 证明接口在主要业务分支下可用
- 覆盖不同场景输入

如有必要，再补：
- 自动补参能力验证
- 必填缺失/非法值异常验证

---

## 六、H5 接口的项目内约定

### 1. 登录能力
- 放在 `api/app/h5_login.py`
- 不在测试文件里重复实现登录

### 2. H5 接口封装
- 放在 `api/app/h5_api.py`
- 通过组合 `H5Login` 复用 session

### 3. H5 测试文件
建议命名：
- `tests/test_h5_xxx_interface.py`

---

## 七、当前项目示例

可参考：
- `api/app/h5_api.py`
- `tests/test_h5_agreement_interface.py`
- `tests/test_h5_read_agreement_interface.py`

这些示例体现了：
- 接口层只封装 `quertAppAgreement()`、`readAgreement()`
- 测试层拆分为冒烟、参数覆盖、上游依赖联调
- `DRAW/BIND` 的自动补参能力单独验证
- 合同阅读接口支持“固定数据联通性”与“依赖合同查询结果”的两层测试

---

## 八、什么时候不要过度覆盖

不要一上来做全参数排列组合。优先覆盖：

1. 最常用成功场景
2. 会触发不同逻辑分支的核心参数
3. 必要的缺参/非法值场景

原则：
**先保证接口可用，再覆盖关键分支，最后再补异常边界。**

---

## 九、推荐输出结果

每次新增接口后，至少应产出：
- 1 个接口封装方法
- 1 条冒烟用例
- 1 组参数覆盖用例
- 可选：1 条封装能力验证用例

如果用户要新增 BM 或 H5 接口，优先按以上模板组织代码，而不是把测试逻辑塞进接口封装层。
