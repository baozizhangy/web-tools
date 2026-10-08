#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
测试用例模型
定义测试用例的数据结构，支持数据驱动测试
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class AssertionType(Enum):
    """断言类型枚举"""
    CODE = "code"
    MESSAGE = "message"
    FIELD = "field"
    FIELD_EXISTS = "field_exists"
    JSONPATH = "jsonpath"
    DB_EXISTS = "db_exists"
    DB_FIELD = "db_field"
    REDIS_EXISTS = "redis_exists"
    CUSTOM = "custom"


class StepType(Enum):
    """步骤类型枚举"""
    API = "api"
    DB = "db"
    REDIS = "redis"
    MOCK = "mock"


@dataclass
class SetupStep:
    """前置步骤"""
    type: str  # StepType
    description: str = ""
    # DB相关
    sql: Optional[str] = None
    table: Optional[str] = None
    db_config: Optional[Dict] = None
    # Redis相关
    key: Optional[str] = None
    value: Optional[Any] = None
    expire: Optional[int] = None
    redis_config: Optional[Dict] = None
    # Mock相关
    url: Optional[str] = None
    data: Optional[Dict] = None
    method: str = "POST"
    # API调用相关
    api_func: Optional[Any] = None
    api_params: Optional[Dict] = None
    extract_mappings: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict:
        """转换为字典"""
        result = {"type": self.type}
        if self.description:
            result["description"] = self.description

        # 根据类型添加相应字段
        if self.type == "db":
            if self.sql:
                result["sql"] = self.sql
            if self.db_config:
                result["db_config"] = self.db_config

        elif self.type == "redis":
            if self.key:
                result["key"] = self.key
            if self.value:
                result["value"] = self.value
            if self.expire:
                result["expire"] = self.expire
            if self.redis_config:
                result["redis_config"] = self.redis_config

        elif self.type == "mock":
            if self.url:
                result["url"] = self.url
            if self.data:
                result["data"] = self.data
            if self.method:
                result["method"] = self.method

        elif self.type == "api":
            if self.api_func:
                result["api_func"] = self.api_func
            if self.api_params:
                result["api_params"] = self.api_params
            if self.extract_mappings:
                result["extract_mappings"] = self.extract_mappings

        return result


@dataclass
class TeardownStep:
    """后置清理步骤"""
    type: str  # StepType
    description: str = ""
    # DB清理
    table: Optional[str] = None
    condition: Optional[str] = None
    db_config: Optional[Dict] = None
    # Redis清理
    key: Optional[str] = None
    redis_config: Optional[Dict] = None

    def to_dict(self) -> Dict:
        """转换为字典"""
        result = {"type": self.type}
        if self.description:
            result["description"] = self.description

        if self.type == "db":
            if self.table:
                result["table"] = self.table
            if self.condition:
                result["condition"] = self.condition
            if self.db_config:
                result["db_config"] = self.db_config

        elif self.type == "redis":
            if self.key:
                result["key"] = self.key
            if self.redis_config:
                result["redis_config"] = self.redis_config

        return result


@dataclass
class Assertion:
    """断言配置"""
    type: str  # AssertionType
    description: str = ""
    # 通用字段
    soft: bool = False  # 是否软断言
    # 响应断言
    expected: Optional[Any] = None
    code_field: str = "code"
    msg_field: str = "msg"
    expected_msg: Optional[str] = None
    # 字段断言
    field_path: Optional[str] = None
    # JSONPath断言
    json_path: Optional[str] = None
    # 数据库断言
    sql: Optional[str] = None
    field: Optional[str] = None
    db_config: Optional[Dict] = None
    # Redis断言
    key: Optional[str] = None
    redis_config: Optional[Dict] = None
    # 自定义断言
    condition: Optional[bool] = None
    error_msg: Optional[str] = None

    def to_dict(self) -> Dict:
        """转换为字典，用于断言执行"""
        result = {"type": self.type}

        if self.type == "code":
            result["expected"] = self.expected
            result["code_field"] = self.code_field
            result["soft"] = self.soft

        elif self.type == "message":
            result["expected_msg"] = self.expected_msg
            result["msg_field"] = self.msg_field
            result["soft"] = self.soft

        elif self.type == "field":
            result["field_path"] = self.field_path
            result["expected"] = self.expected
            result["soft"] = self.soft

        elif self.type == "field_exists":
            result["field_path"] = self.field_path
            result["soft"] = self.soft

        elif self.type == "jsonpath":
            result["json_path"] = self.json_path
            result["expected"] = self.expected
            result["soft"] = self.soft

        elif self.type == "db_exists":
            result["sql"] = self.sql
            if self.db_config:
                result["db_config"] = self.db_config
            result["soft"] = self.soft

        elif self.type == "db_field":
            result["sql"] = self.sql
            result["field"] = self.field
            result["expected"] = self.expected
            if self.db_config:
                result["db_config"] = self.db_config
            result["soft"] = self.soft

        elif self.type == "redis_exists":
            result["key"] = self.key
            if self.redis_config:
                result["redis_config"] = self.redis_config
            result["soft"] = self.soft

        elif self.type == "custom":
            result["condition"] = self.condition
            result["error_msg"] = self.error_msg
            result["soft"] = self.soft

        return result


@dataclass
class TestCaseModel:
    """测试用例模型"""
    case_id: str  # 用例ID
    title: str  # 用例标题
    description: str = ""  # 用例描述

    # 请求参数
    request_data: Dict[str, Any] = field(default_factory=dict)

    # 前置步骤
    setup_steps: List[SetupStep] = field(default_factory=list)

    # 断言配置
    assertions: List[Assertion] = field(default_factory=list)

    # 后置清理步骤
    teardown_steps: List[TeardownStep] = field(default_factory=list)

    # 其他配置
    tags: List[str] = field(default_factory=list)  # 标签
    priority: str = "P2"  # 优先级: P0/P1/P2/P3
    enabled: bool = True  # 是否启用
    retry: int = 0  # 重试次数
    timeout: int = 30  # 超时时间（秒）

    def get_setup_steps_dict(self) -> List[Dict]:
        """获取前置步骤字典列表"""
        return [step.to_dict() for step in self.setup_steps]

    def get_teardown_steps_dict(self) -> List[Dict]:
        """获取后置清理步骤字典列表"""
        return [step.to_dict() for step in self.teardown_steps]

    def get_assertions_dict(self) -> List[Dict]:
        """获取断言配置字典列表"""
        return [assertion.to_dict() for assertion in self.assertions]

    def add_setup_step(self, step: SetupStep):
        """添加前置步骤"""
        self.setup_steps.append(step)

    def add_assertion(self, assertion: Assertion):
        """添加断言"""
        self.assertions.append(assertion)

    def add_teardown_step(self, step: TeardownStep):
        """添加后置步骤"""
        self.teardown_steps.append(step)

    def to_dict(self) -> Dict:
        """转换为完整字典"""
        return {
            "case_id": self.case_id,
            "title": self.title,
            "description": self.description,
            "request_data": self.request_data,
            "setup_steps": self.get_setup_steps_dict(),
            "assertions": self.get_assertions_dict(),
            "teardown_steps": self.get_teardown_steps_dict(),
            "tags": self.tags,
            "priority": self.priority,
            "enabled": self.enabled,
            "retry": self.retry,
            "timeout": self.timeout
        }


@dataclass
class ScenarioModel:
    """场景测试模型（接口串联）"""
    scenario_id: str  # 场景ID
    title: str  # 场景标题
    description: str = ""  # 场景描述

    # 场景中的步骤（每个步骤是一个接口调用）
    steps: List[Dict[str, Any]] = field(default_factory=list)

    # 场景级别的前置步骤
    setup_steps: List[SetupStep] = field(default_factory=list)

    # 场景级别的后置清理
    teardown_steps: List[TeardownStep] = field(default_factory=list)

    # 其他配置
    tags: List[str] = field(default_factory=list)
    priority: str = "P2"
    enabled: bool = True

    def add_step(self, step_name: str, api_func: Any, request_data: Dict,
                 extract_mappings: Dict[str, str] = None,
                 assertions: List[Assertion] = None):
        """
        添加场景步骤

        Args:
            step_name: 步骤名称
            api_func: API函数
            request_data: 请求数据（支持变量替换）
            extract_mappings: 需要提取到上下文的数据映射
            assertions: 该步骤的断言
        """
        step = {
            "step_name": step_name,
            "api_func": api_func,
            "request_data": request_data,
            "extract_mappings": extract_mappings or {},
            "assertions": [a.to_dict() for a in assertions] if assertions else []
        }
        self.steps.append(step)

    def get_setup_steps_dict(self) -> List[Dict]:
        """获取前置步骤字典列表"""
        return [step.to_dict() for step in self.setup_steps]

    def get_teardown_steps_dict(self) -> List[Dict]:
        """获取后置清理步骤字典列表"""
        return [step.to_dict() for step in self.teardown_steps]


if __name__ == '__main__':
    # 使用示例

    # 示例1: 创建单接口测试用例（工单创建接口）
    test_case = TestCaseModel(
        case_id="test_workorder_create_001",
        title="创建工单",
        description="创建工单接口测试"
    )

    # 设置请求数据（使用login_test_data.yaml中的数据进行变量替换）
    test_case.request_data = {
        "categoryCode": "APPLY",
        "subCategoryCode": "",
        "urgencyLevel": "URGENT",
        "userNo": "${userNo}",
        "loanNo": "${loanNo}",
        "content": "创建工单",
        "handlerId": 1,
        "deptId": "100",
        "systemCode": "widek"
    }
    test_case.add_setup_step(SetupStep(
        type="db",
        description="删除已存在的测试用户",
        sql="DELETE FROM users WHERE username='testuser001'"
    ))
    # 添加断言
    test_case.add_assertion(Assertion(
        type="code",
        description="验证响应码",
        expected="0"
    ))

    test_case.add_assertion(Assertion(
        type="field_exists",
        description="验证orderNo存在",
        field_path="data.orderNo"
    ))

    print("测试用例模型:")
    print(test_case.to_dict())

    # 示例2: 创建场景测试（接口串联）
    scenario = ScenarioModel(
        scenario_id="scenario_credit_001",
        title="授信流程",
        description="完整的授信流程测试"
    )

    # 步骤1: 登录
    scenario.add_step(
        step_name="用户登录",
        api_func=None,  # 实际使用时传入API函数
        request_data={"mobile": "13800138000", "code": "123456"},
        extract_mappings={"token": "data.token", "user_id": "data.userId"},
        assertions=[
            Assertion(type="code", expected="0")
        ]
    )

    # 步骤2: 创建授信流程（使用上一步的token）
    scenario.add_step(
        step_name="创建授信流程",
        api_func=None,
        request_data={"token": "${token}", "userId": "${user_id}"},
        extract_mappings={"flow_no": "data.flowNo"},
        assertions=[
            Assertion(type="code", expected="0"),
            Assertion(type="field_exists", field_path="data.flowNo")
        ]
    )

    print("\n场景测试模型:")
    print(f"场景ID: {scenario.scenario_id}")
    print(f"步骤数: {len(scenario.steps)}")