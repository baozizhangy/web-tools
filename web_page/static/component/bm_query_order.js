import ChannelSelector from './channel-selector.js';
import {injectToolShellStyles} from './common/uiShell.js';

export default {
    name: 'query-order',
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
        <el-card shadow="hover" class="tool-shell__card" style="max-width: 860px;">
          <div class="tool-shell__inner">
            <div class="tool-shell__hero tool-shell__hero--amber">
              <div class="tool-shell__hero-content">
                <div>
                  <div class="tool-shell__eyebrow">ORDER STATUS</div>
                  <div class="tool-shell__title">选择借据状态，进行放款</div>
                  <div class="tool-shell__desc">查询最新一笔借据的放款状态，查询后会自动执行放款xxl-job</div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">渠道状态</div>
                    <div class="tool-shell__stat-value">{{ selectChannelItem || '未选择' }}</div>
                  </div>
                </div>
              </div>
            </div>

            <el-form label-position="top">
              <div class="tool-shell__panel tool-shell__panel--soft">
                <div class="tool-shell__panel-title">查询参数</div>
                <div class="tool-shell__panel-desc">
                  输入手机号并选择渠道后，可期望的借据状态来控制最新待放款借据的终态。
                </div>
                <el-row :gutter="20">
                  <el-col :xs="24" :md="12">
                    <el-form-item label="手机号">
                      <el-input
                          class="input_box"
                          type="text"
                          v-model="Mobile"
                          placeholder="用户手机号明文"
                          style="width: 100%"
                          clearable
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="12">
                    <channel-selector
                        v-model="selectChannelItem"
                    />
                  </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :xs="24" :md="12">
                    <el-form-item label="借据终态">
                      <el-select
                          v-model="loanQueryStatus"
                          placeholder="请选择期望的借据终态"
                          style="width: 100%"
                      >
                        <el-option
                            v-for="item in loanQueryStatusOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="12">
                    <el-form-item label="选择资方">
                      <el-select
                          v-model="fundCode"
                          placeholder="指定资金放款/单资方黑暗期时选择资方"
                          style="width: 100%"
                          :disabled="!needFundCode"
                          clearable
                          filterable
                      >
                        <el-option
                            v-for="option in fundCodes"
                            :key="option.value"
                            :label="option.label"
                            :value="option.value"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                <div class="tool-shell__actions">
                  <el-button
                      class="tool-shell__primary-btn"
                      id="submitCreditBtn"
                      @click="QueryOrder"
                      :loading="isQuerying"
                      :disabled="isQuerying"
                      type="primary"
                  >
                    查询放款状态
                  </el-button>
                </div>
              </div>

              <div class="tool-shell__result">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">查询结果</div>
                    <div class="tool-shell__result-desc">借据的状态</div>
                  </div>
                  <div class="tool-shell__result-tag">Status Output</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input
                      type="textarea"
                      :autosize="{minRows:8,maxRows:300}"
                      placeholder="最新一笔借据放款状态"
                      v-model="query_order_info"
                      style="width: 100%">
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
            selectChannelItem: null,
            Mobile: '',
            loanQueryStatus: 'SUCCESS',
            fundCode: '',
            loanQueryStatusOptions: [
                {label: '放款成功', value: 'SUCCESS'},
                {label: '指定资金放款', value: 'SPECIFIED_FUND'},
                {label: '全部资金匹配失败', value: 'ALL_FUND_MATCH_FAIL'},
                {label: '资方黑暗期', value: 'BLACK_TIME'},
                {label: '单资方黑暗期', value: 'FUND_BLACK_TIME'},
                {label: '风险拒绝', value: 'RISK_REJECT'},
            ],
            order_info: '',
            query_order_info: '',
            isQuerying: false,
            fundCodes: [
                {
                    label: '众邦',
                    value: 'ZBANK_E8',
                    title: '众邦',
                },
                {
                    label: '苏商',
                    value: 'ALLINSUSHANG_F24',
                    title: '苏商',
                },
                {
                    label: '蓝海',
                    value: 'ALLINBLUEOCEAN_F24',
                    title: '蓝海',
                },
                {
                    label: '中黔联',
                    value: 'ZHONGQIANLIAN_F36',
                    title: '中黔联',
                },
            ],
        }
    },
    computed: {
        needFundCode() {
            return ['SPECIFIED_FUND', 'FUND_BLACK_TIME'].includes(this.loanQueryStatus);
        },
    },
    methods: {
        async QueryOrder() {
            this.query_order_info = '====根据选择状态触发用户{}放款流程，流程复杂，时间稍长，耐心等候！！！！！===='.replace('{}', this.Mobile) + '\n';
            console.log('查看环境是否正常加载：', this.selectedEnv);
            if (!this.selectChannelItem) {
                this.$message.error('请选择授信通过的渠道！');
                return;
            }
            if (this.needFundCode && !this.fundCode) {
                this.$message.error('当前场景需要选择 fund_code！');
                return;
            }
            if (this.loanQueryStatus === 'RISK_REJECT' && !String(this.Mobile || '').startsWith('133')) {
                this.$alert('受风险条件限制，只能处理手机号133开头用户的借据；不是133开头的请更换用户。', '风险拒绝场景提示', {
                    confirmButtonText: '知道了',
                    type: 'warning',
                });
                return;
            }
            const data = {
                mobile: this.Mobile,
                env: this.selectedEnv,
                channel: this.selectChannelItem,
                loanQueryStatus: this.loanQueryStatus,
                fundCode: this.needFundCode ? this.fundCode : '',
            }
            console.log('本次请求数据', data);
            let query_url = 'api/query_order';

            this.isQuerying = true;
            try {
                const response = await fetch(query_url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                console.log('查询借据状态返回结果', response)
                console.log('查询借据状态返回结果', response.ok)
                if (!response.ok) {
                    console.error('请求失败:', response.status, response.statusText);
                    this.query_order_info += '请求失败，请稍后再试';
                    alert('请求失败，请稍后再试')
                    return;
                }

                const contentType = response.headers.get('Content-Type') || '';
                if (contentType.includes('text/event-stream')) {
                    await this.readStreamResponse(response);
                    return;
                }

                const result = await response.json();
                this.appendQueryResult(result);
            } catch (error) {
                console.error('查询借据状态异常:', error);
                this.query_order_info += `\n请求异常：${error.message || error}\n`;
            } finally {
                this.isQuerying = false;
            }
        },
        async readStreamResponse(response) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';

            while (true) {
                const {done, value} = await reader.read();
                if (done) {
                    break;
                }
                buffer += decoder.decode(value, {stream: true});
                const chunks = buffer.split('\n\n');
                buffer = chunks.pop() || '';

                chunks.forEach((chunk) => this.handleStreamChunk(chunk));
            }

            if (buffer.trim()) {
                this.handleStreamChunk(buffer);
            }
        },
        handleStreamChunk(chunk) {
            const lines = chunk.split('\n').filter((line) => line.startsWith('data:'));
            lines.forEach((line) => {
                const rawData = line.replace(/^data:\s*/, '').trim();
                if (!rawData) {
                    return;
                }
                try {
                    const payload = JSON.parse(rawData);
                    if (payload.type === 'progress') {
                        this.query_order_info += `${payload.message || ''}\n`;
                    } else if (payload.type === 'done') {
                        this.query_order_info += '\n====放款流程执行完成====\n';
                        this.appendQueryResult(payload.result || payload);
                    } else if (payload.type === 'error') {
                        this.query_order_info += `\n执行异常：${payload.message || JSON.stringify(payload)}\n`;
                    } else {
                        this.query_order_info += `${JSON.stringify(payload)}\n`;
                    }
                } catch (error) {
                    this.query_order_info += `${rawData}\n`;
                }
            });
        },
        appendQueryResult(result) {
            let message_info = '';
            if (result.success === 'lcs_success') {
                message_info = '借据放款成功';
            } else if (result.success === 'lcs_fail') {
                message_info = 'lps脚本执行完成，lcs脚本待执行，可再次请求触发lcs脚本执行';
            } else if (result.success === 200) {
                message_info = '最新一笔借据放款成功';
            } else if (result.success === 'fail') {
                message_info = '最后一笔借据不是放款中借据';
            } else if (result.success === 'lcs_wait') {
                message_info = '无可用资方导致放款失败';
            } else if (result.res) {
                message_info = result.res;
            } else {
                message_info = '借据查询失败，检查数据';
            }
            this.query_order_info += '\n' + message_info + '\n';
        },
    },
    mounted() {
        injectToolShellStyles();
    }
}
