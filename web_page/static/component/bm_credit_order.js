import {callApi} from '../api/http.js'
import ChannelSelector from './channel-selector.js';
import { injectToolShellStyles } from './common/uiShell.js';

export default {
    name: 'credit-order',
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
            <div class="tool-shell__hero tool-shell__hero--violet tool-shell__hero--compact">
              <div class="tool-shell__hero-content">
                <div>
                  <div class="tool-shell__eyebrow">ORDER CREATOR</div>
                  <div class="tool-shell__title">创建借据工作台</div>
                  <div class="tool-shell__desc">保持单入口操作，通过下拉框选择无权益或有权益借款，减少切换带来的打断感。</div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">借据类型</div>
                    <div class="tool-shell__stat-value">{{ orderTypeLabel }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="tool-shell__compact-grid">
              <div class="tool-shell__panel tool-shell__panel--soft tool-shell__panel--compact">
                <div class="tool-shell__panel-head">
                  <div>
                    <div class="tool-shell__panel-title">借款参数</div>
                    <div class="tool-shell__panel-desc">先选择渠道和借据类型，再填写手机号、期数、金额；有权益时可继续选择权益类型。</div>
                  </div>
                  <div class="tool-shell__method-pill">ORDER</div>
                </div>

                <el-form label-position="top" class="tool-shell__compact-form">
                  <channel-selector v-model="selectChannelItem" />

                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item label="借据类型">
                      <el-select v-model="selectedOrderItem" placeholder="请选择类型" style="width: 100%;" clearable>
                        <el-option v-for="option in OrderItems" :key="option.value" :label="option.label" :value="option.value" />
                      </el-select>
                    </el-form-item>
                    <el-form-item label="权益类型" v-if="selectedOrderItem === 'Y'">
                      <el-select v-model="selectProfitItem" placeholder="请选择类型" style="width: 100%;" clearable>
                        <el-option v-for="option in ProfitItems" :key="option.value" :label="option.label" :value="option.value" />
                      </el-select>
                    </el-form-item>
                  </div>

                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item label="手机号">
                      <el-input class="input_box" type="text" v-model="Mobile" placeholder="用户手机号明文" style="width: 100%" clearable />
                    </el-form-item>
                    <el-form-item label="借款期数">
                      <el-input class="input_box" type="text" v-model="Term" placeholder="用户借款期数" style="width: 100%" clearable />
                    </el-form-item>
                  </div>

                  <div class="tool-shell__compact-fields tool-shell__compact-fields--single">
                    <el-form-item label="借款金额">
                      <el-input class="input_box" type="text" v-model="amt" placeholder="用户借款金额" style="width: 100%" clearable />
                    </el-form-item>
                  </div>

                  <div class="tool-shell__tip">当前不再使用顶部方法切换；借据类型和权益类型继续通过下拉框选择。</div>
                  <div class="tool-shell__actions tool-shell__actions--compact">
                    <el-button class="tool-shell__primary-btn" @click="CreditOrder" type="primary">提交借款</el-button>
                  </div>
                </el-form>
              </div>

              <div class="tool-shell__result tool-shell__result--compact">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">借款日志</div>
                    <div class="tool-shell__result-desc">展示借据创建过程中的关键返回信息。</div>
                  </div>
                  <div class="tool-shell__result-tag">{{ orderTypeLabel }}</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input type="textarea" :autosize="{minRows:14,maxRows:320}" placeholder="借款日志流程" v-model="order_info" style="width: 100%"></el-input>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    `,
    data() {
        return {
            Mobile: '',
            Term: '',
            amt: '',
            order_info: '',
            selectedOrderItem: null,
            selectChannelItem: null,
            selectProfitItem: null,
            OrderItems: [
                { label: '无权益借款', value: 'N', title: '创建无权益借款' },
                { label: '有权益借款', value: 'Y', title: '创建有权益借款' },
            ],
            ProfitItems: [
                { label: '连续包月', value: '20004', title: '创建连续包月卡' },
                { label: '单月卡', value: '20005', title: '创建单月卡' },
            ],
        }
    },
    computed: {
        orderTypeLabel() {
            if (this.selectedOrderItem === 'Y') return '有权益借款';
            if (this.selectedOrderItem === 'N') return '无权益借款';
            return '未选择';
        },
    },
    methods: {
        async CreditOrder() {
            this.order_info = '====用户借据创建中，勿重复点击====';
            if (!this.selectChannelItem) return this.$message.error('请选择授信渠道！');
            const data = {
                mobile: this.Mobile,
                Term: this.Term || null,
                amt: this.amt || null,
                channel: this.selectChannelItem,
                env: this.selectedEnv,
            };
            if (this.selectChannelItem === 'lxj') {
                if (this.selectedOrderItem === 'Y') data.isPrivilege = 'Y';
                else if (this.selectedOrderItem === 'N') data.isPrivilege = 'N';
            } else if (this.selectChannelItem === 'wacai') {
                data.isPrivilege = 'N';
            }
            if (this.selectedOrderItem === 'Y') {
                if (this.selectProfitItem === '20004') data.profitType = '20004';
                else if (this.selectProfitItem === '20005') data.profitType = '20005';
            }
            const response = await fetch('api/credit_order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (response.ok) {
                const result = await response.json();
                let message_info = '';
                if (result.success === 1) message_info = '二次绑卡借据创建成功，可调用查询借据接口进行放款流程';
                else if (result.success === 0) message_info = '借据创建失败，请检查提交数据';
                else if (result.success === 2) message_info = '借据创建成功，可调用查询借据接口进行放款流程';
                else if (result.success === 3) message_info = '用户授信数据查询失败，创建借据失败，检查用户数据';
                else if (result.success === 4) message_info = '二次绑卡借据创建成功，但是mock还款计划修改失败，使用借据放款进度工具进行放款和再次修改mock';
                else if (result.success === 5) message_info = '已有未废单的权益，不支持再次购买';
                else if (result.success === 6) message_info = '合同获取失败';
                this.order_info += '\n' + message_info + '\n';
            } else {
                this.order_info += '请求失败，请稍后再试';
                alert('请求失败，请稍后再试')
            }
        }
    },
    mounted() { injectToolShellStyles(); }
}
