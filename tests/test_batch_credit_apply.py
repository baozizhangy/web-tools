"""
批量授信功能测试
- 单用户模式（向后兼容验证）
- 批量模式（SSE 流式输出）

运行方式:
    cd D:\tools\webtools
    python -m pytest tests/test_batch_credit_apply.py -v

或指定单个测试:
    python -m pytest tests/test_batch_credit_apply.py::TestSingleUserCreditApply -v
"""
import json
import os
import sys

# ===== Django 环境初始化 =====
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoWebTools.settings')
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import django
django.setup()

import pytest
from unittest.mock import patch
from django.test import RequestFactory
from djangoWebTools.views import bm_credit_apply


# ===== Fixtures =====

@pytest.fixture
def factory():
    """Django RequestFactory"""
    return RequestFactory()


def _make_request(factory, payload):
    """构造 POST 请求"""
    return factory.post(
        '/api/credit_apply',
        data=json.dumps(payload),
        content_type='application/json'
    )


def _parse_sse_response(response):
    """解析 SSE 流式响应，返回 (progress_messages, done_data, error_data)"""
    assert response['Content-Type'] == 'text/event-stream; charset=utf-8'
    content = b''.join(response.streaming_content).decode('utf-8')
    progress_msgs = []
    done_data = None
    error_data = None
    for line in content.split('\n'):
        if not line.startswith('data: '):
            continue
        json_str = line[6:].strip()
        if not json_str:
            continue
        event = json.loads(json_str)
        if event['type'] == 'progress':
            progress_msgs.append(event['message'])
        elif event['type'] == 'done':
            done_data = event['result']
        elif event['type'] == 'error':
            error_data = event['message']
    return progress_msgs, done_data, error_data


# ===== 单用户模式测试（向后兼容） =====

class TestSingleUserCreditApply:
    """单用户授信模式 — 确保 count=1 时向后兼容"""

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_approve(self, mock_apply, mock_query, factory):
        """单用户授信通过"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_TEST_001', 'mobile': '13800138000',
            'res': '授信返回数据'
        }
        mock_query.return_value = 'PS'

        payload = {
            'mobile': '13800138000', 'name': '张三',
            'id_card': '110101199001011234', 'env': 'BM_SIT',
            'channel': 'lxj', 'risk_type': '36', 'credit_apply': 'credit_apply', 'count': 1,
        }
        response = bm_credit_apply(_make_request(factory, payload))

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['success'] == '授信通过'
        assert 'UR_TEST_001' in data['res']
        assert '13800138000' in data['res']
        mock_apply.assert_called_once()
        mock_query.assert_called_once_with('UR_TEST_001', 'BM_SIT')

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_reject(self, mock_apply, mock_query, factory):
        """单用户授信拒绝"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_TEST_002', 'mobile': '13800138001',
            'res': '授信返回'
        }
        mock_query.return_value = 'RJ'

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 1,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        data = json.loads(response.content)
        assert data['success'] == '授信拒绝'
        assert 'UR_TEST_002' in data['res']

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_timeout(self, mock_apply, mock_query, factory):
        """单用户授信状态查询超时"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_TEST_003', 'mobile': '13800138002',
            'res': '授信返回'
        }
        mock_query.return_value = 'timeout'

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 1,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        data = json.loads(response.content)
        assert data['success'] == '查询超时'

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_result_empty(self, mock_apply, mock_query, factory):
        """单用户授信结果为空（false）"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_TEST_004', 'mobile': '13800138003',
            'res': '授信返回'
        }
        mock_query.return_value = 'false'

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 1,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        data = json.loads(response.content)
        assert data['success'] == '结果为空'

    @patch('djangoWebTools.views.credit_apply')
    def test_apply_code_500(self, mock_apply, factory):
        """单用户授信发起异常（code=500）"""
        mock_apply.return_value = {
            'code': 500, 'res': '授信接口返回错误'
        }

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 1,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        data = json.loads(response.content)
        assert data['success'] == 1
        assert '授信申请发起异常' in data['res']

    @patch('djangoWebTools.views.credit_apply')
    def test_crash_fail(self, mock_apply, factory):
        """单用户撞库失败"""
        mock_apply.return_value = '撞库失败'

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 1,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        data = json.loads(response.content)
        assert data['success'] == 2
        assert '准入检查失败' in data['res']

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_count_defaults_to_1(self, mock_apply, mock_query, factory):
        """count 不传时默认走单用户模式（JSON 响应）"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_DEF', 'mobile': '13800000000',
            'res': 'ok'
        }
        mock_query.return_value = 'PS'

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply',
        }
        response = bm_credit_apply(_make_request(factory, payload))
        data = json.loads(response.content)
        assert data['success'] == '授信通过'
        assert response['Content-Type'] != 'text/event-stream'

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_credit_reject_type(self, mock_apply, mock_query, factory):
        """单用户授信拒绝类型（credit_reject）"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_REJ', 'mobile': '13800138005',
            'res': '授信返回'
        }
        mock_query.return_value = 'RJ'

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_reject', 'count': 1,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        data = json.loads(response.content)
        assert data['success'] == '授信拒绝'

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_manual_user_info_passed_through(self, mock_apply, mock_query, factory):
        """单用户模式下手动填写的用户信息被正确传递"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_MANUAL', 'mobile': '13912345678',
            'res': 'ok'
        }
        mock_query.return_value = 'PS'

        payload = {
            'mobile': '13912345678', 'name': '李四',
            'id_card': '320101199001011234', 'env': 'BM_SIT',
            'channel': 'lxj', 'risk_type': '36', 'credit_apply': 'credit_apply', 'count': 1,
        }
        bm_credit_apply(_make_request(factory, payload))

        # 验证传参正确
        call_args = mock_apply.call_args
        assert call_args[0][0] == '13912345678'  # mobile
        assert call_args[0][1] == '李四'          # name
        assert call_args[0][2] == '320101199001011234'  # id_card


# ===== 批量模式测试 =====

class TestBatchCreditApply:
    """批量授信模式 — SSE 流式输出"""

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_all_pass(self, mock_apply, mock_query, factory):
        """批量 3 个全部授信通过"""
        mock_apply.side_effect = [
            {'code': 200, 'user_no': 'UR_B1', 'mobile': 'M001', 'res': 'ok'},
            {'code': 200, 'user_no': 'UR_B2', 'mobile': 'M002', 'res': 'ok'},
            {'code': 200, 'user_no': 'UR_B3', 'mobile': 'M003', 'res': 'ok'},
        ]
        mock_query.side_effect = ['PS', 'PS', 'PS']

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 3,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        msgs, done, err = _parse_sse_response(response)

        assert err is None
        assert any('开始批量发起 3 个授信申请' in m for m in msgs), f"缺少发起消息: {msgs}"
        assert any('开始并发查询授信状态' in m for m in msgs), f"缺少查询消息: {msgs}"
        assert done is not None, "缺少 done 事件"
        assert done['success'] == '批量授信完成'
        assert done['data']['total'] == 3
        assert done['data']['passed'] == 3
        assert done['data']['rejected'] == 0
        assert done['data']['timeout'] == 0
        assert done['data']['empty'] == 0
        assert done['data']['apply_fail'] == 0
        assert done['data']['crash_fail'] == 0
        assert '授信通过 3 个' in done['res']

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_mixed_results(self, mock_apply, mock_query, factory):
        """批量 4 个：1通过 + 1拒绝 + 1超时 + 1发起失败"""
        mock_apply.side_effect = [
            {'code': 200, 'user_no': 'UR_M1', 'mobile': 'MA', 'res': 'ok'},
            {'code': 200, 'user_no': 'UR_M2', 'mobile': 'MB', 'res': 'ok'},
            {'code': 200, 'user_no': 'UR_M3', 'mobile': 'MC', 'res': 'ok'},
            {'code': 500, 'res': '授信接口异常'},
        ]
        # 只有前3个成功发起的需要查询状态
        mock_query.side_effect = ['PS', 'RJ', 'timeout']

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 4,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        _, done, _ = _parse_sse_response(response)

        assert done['data']['total'] == 4
        assert done['data']['passed'] == 1
        assert done['data']['rejected'] == 1
        assert done['data']['timeout'] == 1
        assert done['data']['apply_fail'] == 1
        assert done['data']['crash_fail'] == 0

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_all_crash_fail(self, mock_apply, mock_query, factory):
        """批量全部撞库失败 —— 不会进入 Phase 2 查询"""
        mock_apply.side_effect = ['撞库失败'] * 3

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 3,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        _, done, _ = _parse_sse_response(response)

        assert done['data']['crash_fail'] == 3
        assert done['data']['passed'] == 0
        # query_risk_status 不应被调用
        mock_query.assert_not_called()

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_empty_result_counted(self, mock_apply, mock_query, factory):
        """批量中包含结果为空（false）的case"""
        mock_apply.side_effect = [
            {'code': 200, 'user_no': 'UR_E1', 'mobile': 'ME1', 'res': 'ok'},
            {'code': 200, 'user_no': 'UR_E2', 'mobile': 'ME2', 'res': 'ok'},
        ]
        mock_query.side_effect = ['PS', 'false']

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 2,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        _, done, _ = _parse_sse_response(response)

        assert done['data']['passed'] == 1
        assert done['data']['empty'] == 1

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_details_ordered(self, mock_apply, mock_query, factory):
        """批量详情按提交顺序排列（idx 0,1,2...）"""
        mock_apply.side_effect = [
            {'code': 200, 'user_no': 'UR_AA', 'mobile': 'MAA', 'res': 'ok'},
            {'code': 200, 'user_no': 'UR_BB', 'mobile': 'MBB', 'res': 'ok'},
            {'code': 200, 'user_no': 'UR_CC', 'mobile': 'MCC', 'res': 'ok'},
        ]
        mock_query.side_effect = ['PS', 'RJ', 'PS']

        payload = {
            'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 3,
        }
        response = bm_credit_apply(_make_request(factory, payload))
        _, done, _ = _parse_sse_response(response)

        details = done['data']['details']
        assert len(details) == 3
        assert details[0]['user_no'] == 'UR_AA'
        assert details[1]['user_no'] == 'UR_BB'
        assert details[2]['user_no'] == 'UR_CC'

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_force_random_users(self, mock_apply, mock_query, factory):
        """批量模式下即使传入手机号/姓名/身份证，也强制用 None（随机生成）"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_RAND', 'mobile': 'MR', 'res': 'ok'
        }
        mock_query.return_value = 'PS'

        payload = {
            'mobile': '13900001111', 'name': '王五',
            'id_card': '320101199001010001', 'env': 'BM_SIT',
            'channel': 'lxj', 'risk_type': '36',
            'credit_apply': 'credit_apply', 'count': 2,
        }
        bm_credit_apply(_make_request(factory, payload))

        for call_args in mock_apply.call_args_list:
            args = call_args[0]
            assert args[0] is None, f"批量模式 mobile 应为 None，实际: {args[0]}"
            assert args[1] is None, f"批量模式 name 应为 None，实际: {args[1]}"
            assert args[2] is None, f"批量模式 id_card 应为 None，实际: {args[2]}"

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_channel_and_risk_type_consistent(self, mock_apply, mock_query, factory):
        """批量模式下渠道和风险类型在每次调用中保持一致"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_CONS', 'mobile': 'MCONS', 'res': 'ok'
        }
        mock_query.return_value = 'PS'

        payload = {
            'env': 'BM_DEV', 'channel': 'tongcheng', 'risk_type': '24',
            'credit_apply': 'credit_reject', 'count': 3,
        }
        bm_credit_apply(_make_request(factory, payload))

        for call_args in mock_apply.call_args_list:
            kwargs = call_args[1]
            assert kwargs['channel'] == 'tongcheng'
            assert kwargs['risk_type'] == '24'
            assert kwargs['credit_apply'] == 'credit_reject'
            assert kwargs['env'] == 'BM_DEV'

    @patch('djangoWebTools.views.query_risk_status')
    @patch('djangoWebTools.views.credit_apply')
    def test_single_user_still_works_with_manual_info(self, mock_apply, mock_query, factory):
        """单用户模式仍可手动填写信息 —— 向前兼容关键验证"""
        mock_apply.return_value = {
            'code': 200, 'user_no': 'UR_OLD', 'mobile': '13999999999',
            'res': 'ok'
        }
        mock_query.return_value = 'PS'

        # 模拟原有前端调用（不传 count，传完整三要素）
        payload = {
            'mobile': '13999999999',
            'name': '赵六',
            'id_card': '110101199501011234',
            'credit_apply': 'credit_apply',
            'risk_type': '36',
            'env': 'BM_SIT',
            'channel': 'lxj',
        }
        response = bm_credit_apply(_make_request(factory, payload))
        data = json.loads(response.content)

        assert data['success'] == '授信通过'
        assert 'UR_OLD' in data['res']
        assert '13999999999' in data['res']


# ===== count 参数边界校验 =====

class TestCountParameterValidation:
    """count 参数校验"""

    def test_count_exceeds_10_clamped(self, factory):
        """count=15 → 限制为 10"""
        with patch('djangoWebTools.views.credit_apply') as mock_apply, \
             patch('djangoWebTools.views.query_risk_status') as mock_query:
            mock_apply.return_value = {
                'code': 200, 'user_no': 'UR_C', 'mobile': 'MC', 'res': 'ok'
            }
            mock_query.return_value = 'PS'

            payload = {
                'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
                'credit_apply': 'credit_apply', 'count': 15,
            }
            response = bm_credit_apply(_make_request(factory, payload))
            assert response['Content-Type'] == 'text/event-stream; charset=utf-8'
            # 先消费 SSE 流（触发 worker 线程执行），再检查调用次数
            _parse_sse_response(response)
            assert mock_apply.call_count == 10

    def test_count_zero_defaults_to_1(self, factory):
        """count=0 → 默认走单用户模式"""
        with patch('djangoWebTools.views.credit_apply') as mock_apply, \
             patch('djangoWebTools.views.query_risk_status') as mock_query:
            mock_apply.return_value = {
                'code': 200, 'user_no': 'UR_Z', 'mobile': 'MZ', 'res': 'ok'
            }
            mock_query.return_value = 'PS'

            payload = {
                'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
                'credit_apply': 'credit_apply', 'count': 0,
            }
            response = bm_credit_apply(_make_request(factory, payload))
            data = json.loads(response.content)
            assert data['success'] == '授信通过'
            assert mock_apply.call_count == 1

    def test_count_negative_defaults_to_1(self, factory):
        """count=-5 → 默认走单用户模式"""
        with patch('djangoWebTools.views.credit_apply') as mock_apply, \
             patch('djangoWebTools.views.query_risk_status') as mock_query:
            mock_apply.return_value = {
                'code': 200, 'user_no': 'UR_NEG', 'mobile': 'MNEG', 'res': 'ok'
            }
            mock_query.return_value = 'PS'

            payload = {
                'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
                'credit_apply': 'credit_apply', 'count': -5,
            }
            response = bm_credit_apply(_make_request(factory, payload))
            data = json.loads(response.content)
            assert data['success'] == '授信通过'
            assert mock_apply.call_count == 1

    def test_count_invalid_string_defaults_to_1(self, factory):
        """count='abc' → 默认走单用户模式"""
        with patch('djangoWebTools.views.credit_apply') as mock_apply, \
             patch('djangoWebTools.views.query_risk_status') as mock_query:
            mock_apply.return_value = {
                'code': 200, 'user_no': 'UR_STR', 'mobile': 'MSTR', 'res': 'ok'
            }
            mock_query.return_value = 'PS'

            payload = {
                'env': 'BM_SIT', 'channel': 'lxj', 'risk_type': '36',
                'credit_apply': 'credit_apply', 'count': 'abc',
            }
            response = bm_credit_apply(_make_request(factory, payload))
            data = json.loads(response.content)
            assert data['success'] == '授信通过'
            assert mock_apply.call_count == 1
