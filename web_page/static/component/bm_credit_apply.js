import ChannelSelector from './channel-selector.js';
import {injectToolShellStyles} from './common/uiShell.js';

const DEFAULT_APPLY_URL = 'api/credit_apply';
const APPLY_ITEMS = [
    {
        label: '授信通过用户',
        value: 'credit_apply',
        title: '创建用户授信',
    },
    {
        label: '授信拒绝用户',
        value: 'credit_reject',
        title: '创建用户授信',
    },
];
const RISK_TYPES = [
    {
        label: '36用户',
        value: '36',
        title: '36用户',
    },
    {
        label: '24用户',
        value: '24',
        title: '24用户',
    },
];

export default {
    name: 'credit-apply',
    components: {
        'channel-selector': ChannelSelector
    },
    props: {
        selectedEnv: {
            type: String,
            required: true
        },
    },
    template: `
      <div class="tool-shell">
        <el-card shadow="hover" class="tool-shell__card">
          <div class="tool-shell__inner">
            <div class="tool-shell__hero tool-shell__hero--blue">
              <div class="tool-shell__hero-content">
                <div>
                  <div class="tool-shell__eyebrow">BM CREDIT WORKBENCH</div>
                  <div class="tool-shell__title">授信申请</div>
                  <div class="tool-shell__desc">授信申请默认 sit 环境，可切换环境、渠道、36 和 24
                    代表匹配不同类型资金的用户。
                  </div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">风险类型</div>
                    <div class="tool-shell__stat-value">{{ selectedRiskType || '未选择' }}</div>
                  </div>
                </div>
              </div>
            </div>

            <el-form label-position="top">
              <el-row :gutter="20">
                <el-col :xs="24" :md="11">
                  <div class="tool-shell__panel tool-shell__panel--soft">
                    <div class="tool-shell__panel-title">基础配置</div>
                    <div class="tool-shell__panel-desc">先选择节点、风险类型和渠道，再按需填写用户三要素。</div>

                    <el-form-item label="选择授信结果">
                      <el-select
                          v-model="selectedApplyItem"
                          placeholder="请选择节点"
                          style="width: 100%;"
                          clearable
                          @change="handleApplyItemChange"
                      >
                        <el-option
                            v-for="option in applyItems"
                            :key="option.value"
                            :label="option.label"
                            :value="option.value"
                        />
                      </el-select>
                    </el-form-item>

                    <el-form-item label="选择风险类型">
                      <el-select
                          v-model="selectedRiskType"
                          placeholder="请选择风险类型"
                          style="width: 100%;"
                          clearable
                          @change="handleRiskTypeChange"
                      >
                        <el-option
                            v-for="option in riskTypes"
                            :key="option.value"
                            :label="option.label"
                            :value="option.value"
                        />
                      </el-select>
                    </el-form-item>

                    <channel-selector
                        v-model="selectedChannel"
                        @change="handleChannelChange"
                    />
                  </div>
                </el-col>

                <el-col :xs="24" :md="13">
                  <div class="tool-shell__panel">
                    <div class="tool-shell__panel-title">用户信息</div>
                    <div class="tool-shell__panel-desc">支持留空，系统会按当前流程自动生成随机用户数据。</div>

                    <el-row :gutter="16">
                      <el-col :xs="24" :sm="12">
                        <el-form-item label="手机号">
                          <el-input
                              class="input_box"
                              type="text"
                              v-model.trim="mobile"
                              :placeholder="count > 1 ? '批量模式自动生成' : (selectedApplyItem === 'credit_reject' ? '授信拒绝自动生成(144)' : '为空则随机生成')"
                              style="width: 100%"
                              clearable
                              :disabled="selectedApplyItem === 'credit_reject' || count > 1"
                          />
                        </el-form-item>
                      </el-col>
                      <el-col :xs="24" :sm="12">
                        <el-form-item label="姓名">
                          <el-input
                              class="input_box"
                              type="text"
                              v-model.trim="name"
                              :placeholder="count > 1 ? '批量模式自动生成' : '为空则随机生成'"
                              style="width: 100%"
                              clearable
                              :disabled="count > 1"
                          />
                        </el-form-item>
                      </el-col>
                    </el-row>

                    <el-form-item label="身份证号">
                      <el-input
                          class="input_box"
                          type="text"
                          v-model.trim="idCard"
                          :placeholder="count > 1 ? '批量模式自动生成' : '为空则随机生成'"
                          style="width: 100%"
                          clearable
                          :disabled="count > 1"
                      />
                    </el-form-item>

                    <div class="tool-shell__tip" v-if="count <= 1">提示：授信三要素可为空，为空自动生成数据。</div>

                    <el-form-item label="批量授信数量（1-10）">
                      <el-input-number
                          v-model="count"
                          :min="1"
                          :max="10"
                          :step="1"
                          style="width: 100%;"
                          @change="handleCountChange"
                      />
                      <div class="tool-shell__tip" v-if="count > 1">批量模式下自动随机生成用户信息，不支持手动填写。</div>
                    </el-form-item>

                    <div class="tool-shell__actions">
                      <el-button
                          class="tool-shell__primary-btn"
                          id="submitCreditBtn"
                          @click="creditApply"
                          type="primary"
                          :loading="submitting"
                      >
                        {{ count > 1 ? '批量发起授信（' + count + '个）' : '发起授信' }}
                      </el-button>
                    </div>
                  </div>
                </el-col>
              </el-row>

              <div class="tool-shell__result">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">授信日志</div>
                    <div class="tool-shell__result-desc">实时查看当前授信请求结果与错误信息输出。</div>
                  </div>
                  <div class="tool-shell__result-tag">Live Output</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input
                      type="textarea"
                      :autosize="{ minRows: 8, maxRows: 300 }"
                      placeholder="授信日志"
                      v-model="applyLogInfo"
                      style="width: 100%;"
                  >
                  </el-input>
                </div>
              </div>
            </el-form>
          </div>
        </el-card>
      </div>
    `,
    data() {
        return {
            mobile: '',
            name: '',
            idCard: '',
            count: 1,
            applyLogInfo: '',
            applyUrl: DEFAULT_APPLY_URL,
            riskType: '',
            selectedApplyItem: null,
            selectedChannel: null,
            selectedRiskType: '36',
            submitting: false,
            applyItems: APPLY_ITEMS,
            riskTypes: RISK_TYPES,
        }
    },
    mounted() {
        injectToolShellStyles();
        this.handleRiskTypeChange(this.selectedRiskType);
    },
    methods: {
        handleApplyItemChange(value) {
            console.log('Selected init item:', value);
            this.applyUrl = DEFAULT_APPLY_URL;
            if (value === 'credit_reject') {
                this.mobile = '';
            }
        },
        handleChannelChange(value) {
            this.selectedChannel = value;
        },
        handleRiskTypeChange(value) {
            console.log('Selected risk item:', value);
            this.riskType = value || '';
        },
        handleCountChange(value) {
            // 批量模式下清空用户信息
            if (value > 1) {
                this.mobile = '';
                this.name = '';
                this.idCard = '';
            }
        },
        async creditApply() {
            if (this.submitting) {
                return;
            }

            if (!this.selectedChannel) {
                this.$message.error('请选择发起授信渠道！');
                return;
            }

            const isReject = this.selectedApplyItem === 'credit_reject';
            const isBatch = this.count > 1;

            if (isBatch) {
                this.applyLogInfo = `====批量授信发起中（${this.count}个用户），渠道：${this.selectedChannel}，风险类型：${this.riskType}，勿重复点击====\n`;
            } else {
                this.applyLogInfo = `====授信发起中${isReject ? '授信拒绝(自动生成144手机号)' : (this.mobile || '随机用户')}，勿重复点击====`;
            }
            this.submitting = true;

            const payload = {
                name: isBatch ? null : (this.name || null),
                mobile: isBatch ? null : (isReject ? null : (this.mobile || null)),
                id_card: isBatch ? null : (this.idCard || null),
                credit_apply: this.selectedApplyItem,
                risk_type: this.riskType,
                env: this.selectedEnv,
                channel: this.selectedChannel,
                count: this.count,
            };

            try {
                const response = await fetch(this.applyUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                console.log('creditApply response', response);

                if (!response.ok) {
                    throw new Error(`请求失败: ${response.status} ${response.statusText}`);
                }

                // 批量模式：SSE 流式处理
                if (isBatch) {
                    await this._handleBatchResponse(response);
                    return;
                }

                // 单用户模式：JSON 响应
                const result = await response.json();
                let messageInfo = '';
                if (result.success === "授信通过") {
                    messageInfo = `用户授信成功: ${result.res}`;
                } else if (result.success === "授信拒绝") {
                    messageInfo = `用户授信失败，请检查提交类型、日志${result.res}`;
                } else if (result.success === "查询超时") {
                    messageInfo = `授信处理中，可手动查询:${result.res}`;
                } else if (result.success === "结果为空") {
                    messageInfo = `发起后10秒风险没有收到授信请求，检查lps预授信记录: ${JSON.stringify(result)}`;
                } else {
                    messageInfo = `未知错误: ${JSON.stringify(result)}`;
                }

                this.applyLogInfo += `\n${messageInfo}\n`;
            } catch (error) {
                console.error('creditApply error:', error);
                this.applyLogInfo += `\n请求失败：${error.message}\n`;
                this.$message.error('请求失败，请稍后再试');
            } finally {
                this.submitting = false;
            }
        },
        async _handleBatchResponse(response) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            try {
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n');
                    buffer = lines.pop() || '';

                    for (const line of lines) {
                        if (!line.startsWith('data: ')) continue;
                        const jsonStr = line.slice(6).trim();
                        if (!jsonStr) continue;

                        try {
                            const event = JSON.parse(jsonStr);
                            if (event.type === 'progress') {
                                this.applyLogInfo += `${event.message}\n`;
                            } else if (event.type === 'done') {
                                const r = event.result;
                                this.applyLogInfo += `\n===== ${r.res} =====\n`;
                                if (r.data && r.data.details) {
                                    this.applyLogInfo += '\n--- 明细 ---\n';
                                    r.data.details.forEach((d, i) => {
                                        const statusLabel = {
                                            'PS': '通过', 'RJ': '拒绝', 'timeout': '超时',
                                            'false': '结果为空', 'apply_fail': '发起失败', 'crash_fail': '撞库失败'
                                        }[d.status] || d.status;
                                        this.applyLogInfo += `[${i + 1}] ${d.mobile || 'N/A'} | user_no: ${d.user_no || 'N/A'} | ${statusLabel}\n`;
                                    });
                                }
                                this.applyLogInfo += '\n===== 批量授信结束 =====\n';
                                this.$message.success('批量授信完成，详见日志');
                            } else if (event.type === 'error') {
                                this.applyLogInfo += `\n错误：${event.message}\n`;
                                this.$message.error(event.message);
                            }
                        } catch (parseErr) {
                            console.warn('SSE parse error:', parseErr);
                        }
                    }
                }
            } catch (error) {
                console.error('SSE read error:', error);
                this.applyLogInfo += `\n流读取失败：${error.message}\n`;
                this.$message.error('流读取失败');
            } finally {
                this.submitting = false;
            }
        },
    },
}
