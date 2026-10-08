import {callApi} from '../api/http.js'
import ChannelSelector from './channel-selector.js';
import { injectToolShellStyles } from './common/uiShell.js';

export default {
    name: 'repay-order',
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
        <el-card shadow="hover" class="tool-shell__card tool-shell__card--compact">
          <div class="tool-shell__inner tool-shell__inner--compact">
            <div class="tool-shell__hero tool-shell__hero--teal tool-shell__hero--compact">
              <div class="tool-shell__hero-content">
                <div>
                  <div class="tool-shell__eyebrow">REPAY WORKBENCH</div>
                  <div class="tool-shell__title">借据还款工作台</div>
                  <div class="tool-shell__desc">保持单入口操作，通过下拉框选择发起还款或单笔试算，减少切换带来的打断感。</div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前动作</div>
                    <div class="tool-shell__stat-value">{{ actionLabel }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="tool-shell__compact-grid">
              <div class="tool-shell__panel tool-shell__panel--soft tool-shell__panel--compact">
                <div class="tool-shell__panel-head">
                  <div>
                    <div class="tool-shell__panel-title">还款参数</div>
                    <div class="tool-shell__panel-desc">通过下拉框选择发起还款或单笔试算，再填写对应借据号和还款类型。</div>
                  </div>
                  <div class="tool-shell__method-pill">REPAY</div>
                </div>

                <el-form label-position="top" class="tool-shell__compact-form">
                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item label="执行动作">
                      <el-select v-model="actionType" placeholder="请选择动作" style="width: 100%">
                        <el-option label="发起还款" value="repay" />
                        <el-option label="单笔试算" value="trial" />
                      </el-select>
                    </el-form-item>
                    <el-form-item label="还款类型">
                      <el-select v-model="repayTypeValue" placeholder="请选择类型" style="width: 100%;" clearable @change="RepayItemsChange">
                        <el-option v-for="option in RepayItems" :key="option.value" :label="option.label" :value="option.value" />
                      </el-select>
                    </el-form-item>
                  </div>

                  <div class="tool-shell__compact-fields tool-shell__compact-fields--single">
                    <el-form-item :label="actionType === 'repay' ? '借据号' : '试算借据号'">
                      <el-input class="input_box" type="text" v-model="currentLoanNo" :placeholder="actionType === 'repay' ? '还款借据号' : '试算借据号'" style="width: 100%" clearable />
                    </el-form-item>
                  </div>

                  <channel-selector v-model="selectChannelItem" />

                  <div class="tool-shell__tip tool-shell__tip--teal">当前不再使用顶部方法切换；动作与还款类型继续通过下拉框选择。</div>
                  <div class="tool-shell__actions tool-shell__actions--compact">
                    <el-button class="tool-shell__primary-btn tool-shell__primary-btn--teal" @click="submitCurrentAction" type="primary">
                      {{ actionType === 'repay' ? '发起还款' : '发起试算' }}
                    </el-button>
                  </div>
                </el-form>
              </div>

              <div class="tool-shell__result tool-shell__result--teal tool-shell__result--compact">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">执行日志</div>
                    <div class="tool-shell__result-desc">查看当前动作返回结果与异常信息。</div>
                  </div>
                  <div class="tool-shell__result-tag">{{ actionLabel }}</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input type="textarea" :autosize="{minRows:14,maxRows:320}" :placeholder="actionType === 'repay' ? '触发还款明细' : '试算结果'" v-model="currentResultText"></el-input>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    `,
    data() {
        return {
            actionType: 'repay',
            Loan_no: '',
            trail_loan_no: '',
            repay_order_info: '',
            trail_order_info: '',
            repayTypeValue: null,
            repay_type: null,
            selectChannelItem: null,
            RepayItems: [
                { label: '当期还款', value: 1, title: '当期还款' },
                { label: '逾期还款-当期', value: 2, title: '逾期还款-当期' },
                { label: '整笔提前结清', value: 4, title: '整笔提前结清' }
            ],
        }
    },
    computed: {
        actionLabel() {
            return this.actionType === 'repay' ? '发起还款' : '单笔试算';
        },
        currentLoanNo: {
            get() {
                return this.actionType === 'repay' ? this.Loan_no : this.trail_loan_no;
            },
            set(value) {
                if (this.actionType === 'repay') this.Loan_no = value;
                else this.trail_loan_no = value;
            }
        },
        currentResultText: {
            get() {
                return this.actionType === 'repay' ? this.repay_order_info : this.trail_order_info;
            },
            set(value) {
                if (this.actionType === 'repay') this.repay_order_info = value;
                else this.trail_order_info = value;
            }
        },
    },
    methods: {
        RepayItemsChange(value) {
            if ([1, 2, 4].includes(value)) this.repay_type = value;
            else alert('请选择还款类型');
        },
        submitCurrentAction() {
            if (this.actionType === 'repay') {
                return this.SumitOrder();
            }
            return this.SumitTrial();
        },
        async SumitOrder() {
            this.repay_order_info = `====借据还款申请中：${this.Loan_no}，勿重复点击====\n`;
            if (!this.selectChannelItem) return this.$message.error('请选择授信通过的渠道！');
            const data = { loan_no: this.Loan_no, repay_type: this.repay_type, channel: this.selectChannelItem, env: this.selectedEnv };
            const response = await fetch('api/bm_repay_order', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
            if (response.ok) {
                const result = await response.json();
                let message_info = '';
                if (result.success === 0) message_info = '用户发起还款成功' + result.res;
                else if (result.success === 1) message_info = '用户发起试算异常，请检查提交数据' + result.res;
                else if (result.success === 2) message_info = '发起还款异常，检查提交数据' + result.res;
                else if (result.success === 3) message_info = '特殊场景异常' + result.res;
                this.repay_order_info += `\n${message_info}\n`;
            } else {
                alert('请求失败，请稍后再试');
            }
        },
        async SumitTrial() {
            this.trail_order_info = `====试算发起：${this.trail_loan_no}，勿重复点击====\n`;
            if (!this.selectChannelItem) return this.$message.error('请选择授信通过的渠道！');
            const data = { loan_no: this.trail_loan_no, repay_type: this.repay_type, channel: this.selectChannelItem, env: this.selectedEnv };
            const response = await fetch('api/bm_repay_trail_order', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
            if (response.ok) {
                const result = await response.json();
                let message_info = '';
                if (result.success === 0) message_info = '试算发起结果：' + result.res;
                this.trail_order_info += `\n${message_info}\n`;
            }
        },
    },
    mounted() { injectToolShellStyles(); }
}
