import ChannelSelector from './channel-selector.js';
import {injectToolShellStyles} from './common/uiShell.js';

export default {
    name: 'query-repay-result',
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
            <div class="tool-shell__hero tool-shell__hero--violet">
              <div class="tool-shell__hero-content">
                <div>
                  <div class="tool-shell__eyebrow">REPAY RESULT</div>
                  <div class="tool-shell__title">还款结果查询</div>
                  <div class="tool-shell__desc">查询借据还款状态，支持还款成功、还款失败、部分成功场景</div>
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
                  输入借据号并选择目标还款状态，系统会自动执行相应的还款结果查询流程。
                </div>
                <el-row :gutter="20">
                  <el-col :xs="24" :md="8">
                    <el-form-item label="手机号">
                      <el-input
                          class="input_box"
                          type="text"
                          v-model="mobile"
                          placeholder="请输入手机号"
                          style="width: 100%"
                          clearable
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="8">
                    <el-form-item label="借据号">
                      <el-input
                          class="input_box"
                          type="text"
                          v-model="loanNo"
                          placeholder="请输入借据号 LNxxxx"
                          style="width: 100%"
                          clearable
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="8">
                    <channel-selector
                        v-model="selectChannelItem"
                    />
                  </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :xs="24" :md="12">
                    <el-form-item label="还款状态">
                      <el-select
                          v-model="repayQueryStatus"
                          placeholder="请选择期望的还款状态"
                          style="width: 100%"
                      >
                        <el-option
                            v-for="item in repayQueryStatusOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="12">
                    <el-form-item label="还款期数">
                      <el-select
                          v-model="term"
                          placeholder="请选择还款期数"
                          style="width: 100%"
                          clearable
                      >
                        <el-option
                            v-for="item in termOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                <div class="tool-shell__actions">
                  <el-button
                      class="tool-shell__primary-btn"
                      id="submitRepayQueryBtn"
                      @click="QueryRepayResult"
                      :loading="isQuerying"
                      :disabled="isQuerying"
                      type="primary"
                  >
                    查询还款结果
                  </el-button>
                </div>
              </div>

              <div class="tool-shell__result">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">查询结果</div>
                    <div class="tool-shell__result-desc">还款结果查询流程输出</div>
                  </div>
                  <div class="tool-shell__result-tag">Status Output</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input
                      type="textarea"
                      :autosize="{minRows:8,maxRows:300}"
                      placeholder="还款结果查询流程日志"
                      v-model="queryRepayResultInfo"
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
            selectChannelItem: 'lxj',
            mobile: '',
            loanNo: '',
            repayQueryStatus: 'SUCCESS',
            term: '',
            termOptions: [
                {label: '提前结清', value: 'all'},
                {label: '第1期', value: '1'},
                {label: '第2期', value: '2'},
                {label: '第3期', value: '3'},
                {label: '第4期', value: '4'},
                {label: '第5期', value: '5'},
                {label: '第6期', value: '6'},
                {label: '第7期', value: '7'},
                {label: '第8期', value: '8'},
                {label: '第9期', value: '9'},
                {label: '第10期', value: '10'},
                {label: '第11期', value: '11'},
                {label: '第12期', value: '12'},
            ],
            repayQueryStatusOptions: [
                {label: '还款成功', value: 'SUCCESS'},
                {label: '还款失败', value: 'FAIL'},
                {label: '部分成功', value: 'PARTIAL_SUCCESS'},
            ],
            queryRepayResultInfo: '',
            isQuerying: false,
        }
    },
    mounted() {
        injectToolShellStyles();
    },
    methods: {
        QueryRepayResult() {
            if (!this.mobile) {
                ElementPlus.ElMessage.error('请输入手机号');
                return;
            }
            if (!this.loanNo) {
                ElementPlus.ElMessage.error('请输入借据号');
                return;
            }
            if (!this.selectChannelItem) {
                ElementPlus.ElMessage.error('请选择渠道');
                return;
            }

            this.isQuerying = true;
            this.queryRepayResultInfo = '';

            fetch('/api/query_repay_result', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    mobile: this.mobile,
                    loan_no: this.loanNo,
                    env: this.selectedEnv,
                    channel: this.selectChannelItem,
                    repayQueryStatus: this.repayQueryStatus,
                    term: this.term || null
                })
            }).then(response => {
                const reader = response.body.getReader();
                const decoder = new TextDecoder();

                const processStream = ({done, value}) => {
                    if (done) {
                        this.isQuerying = false;
                        return;
                    }

                    const chunk = decoder.decode(value, {stream: true});
                    const lines = chunk.split('\n');

                    lines.forEach(line => {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.substring(6));
                                if (data.type === 'progress') {
                                    this.queryRepayResultInfo += data.message + '\n';
                                } else if (data.type === 'done') {
                                    this.queryRepayResultInfo += '\n========== 查询完成 ==========\n';
                                    this.queryRepayResultInfo += `结果: ${data.result.res}\n`;
                                    this.queryRepayResultInfo += `状态码: ${data.result.success}\n`;
                                    this.isQuerying = false;

                                    if (data.result.success === 'repay_success' ||
                                        data.result.success === 'repay_fail' ||
                                        data.result.success === 'repay_partial_success') {
                                        ElementPlus.ElMessage.success('还款结果查询完成');
                                    } else {
                                        ElementPlus.ElMessage.warning(data.result.res);
                                    }
                                } else if (data.type === 'error') {
                                    this.queryRepayResultInfo += '\n========== 查询异常 ==========\n';
                                    this.queryRepayResultInfo += `错误: ${data.message}\n`;
                                    this.isQuerying = false;
                                    ElementPlus.ElMessage.error('还款结果查询异常');
                                }
                            } catch (e) {
                                console.error('解析SSE数据失败:', e, line);
                            }
                        }
                    });

                    return reader.read().then(processStream);
                };

                return reader.read().then(processStream);
            }).catch(error => {
                console.error('请求错误:', error);
                this.queryRepayResultInfo += '\n========== 连接异常 ==========\n';
                this.queryRepayResultInfo += `错误: ${error.message}\n`;
                this.isQuerying = false;
                ElementPlus.ElMessage.error('连接异常，请重试');
            });
        }
    }
}
