import { injectToolShellStyles } from './common/uiShell.js';

const PAY_CHANNEL_OPTIONS = [
    { label: '宝付（baofu）', value: 'baofu' },
    { label: '通联（allinpay）', value: 'allinpay' },
    { label: '汇付（huifu）', value: 'huifu' },
    { label: '多通道（all）', value: 'all' },
];

export default {
    name: 'bind-card-submit',
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
                  <div class="tool-shell__eyebrow">H5 BIND CARD</div>
                  <div class="tool-shell__title">H5 绑卡</div>
                  <div class="tool-shell__desc">支持按支付通道触发不同绑卡流程；场景只支持 DRAW / REPAY。</div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前场景</div>
                    <div class="tool-shell__stat-value">{{ bindScene }}</div>
                  </div>
                </div>
              </div>
            </div>

            <el-form label-position="top">
              <div class="tool-shell__panel tool-shell__panel--soft">
                <div class="tool-shell__panel-title">绑卡参数</div>
                <div class="tool-shell__panel-desc">手机号必填；宝付 支持手填卡号；all / allinpay / huifu 自动生成卡号并执行绑卡。</div>

                <el-row :gutter="20">
                  <el-col :xs="24" :md="12">
                    <el-form-item label="手机号（必填）">
                      <el-input
                          class="input_box"
                          type="text"
                          v-model.trim="mobile"
                          placeholder="请输入手机号"
                          clearable
                          style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="12">
                    <el-form-item label="场景">
                      <el-select v-model="bindScene" style="width: 100%" placeholder="请选择场景">
                        <el-option label="DRAW（借款）" value="DRAW" />
                        <el-option label="REPAY（还款）" value="REPAY" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :xs="24" :md="12">
                    <el-form-item label="支付通道">
                      <el-select v-model="payChannel" style="width: 100%" placeholder="请选择支付通道" @change="handlePayChannelChange">
                        <el-option
                            v-for="option in payChannelOptions"
                            :key="option.value"
                            :label="option.label"
                            :value="option.value"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="12">
                    <el-form-item label="银行卡号（非必填）">
                      <el-input
                          class="input_box"
                          type="text"
                          v-model.trim="cardNo"
                          :placeholder="isAutoCardChannel ? '当前通道自动生成卡号，不支持手填' : '不填则自动生成卡号'"
                          :disabled="isAutoCardChannel"
                          clearable
                          style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>

                <div class="tool-shell__tip">
                  <template v-if="isAutoCardChannel">提示：当前通道会自动生成卡号；all / allinpay / huifu 绑卡流程,目前baofu强制绑定：选择通联会绑定宝付+通联。</template>
                  <template v-else>提示：baofu 支持手填卡号；不填写时后端会自动生成。</template>
                </div>

                <div class="tool-shell__actions">
                  <el-button
                      class="tool-shell__primary-btn"
                      type="primary"
                      @click="submitBindCard"
                      :loading="submitting"
                  >
                    提交绑卡
                  </el-button>
                </div>
              </div>

              <div class="tool-shell__result">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">返回结果</div>
                    <div class="tool-shell__result-desc">接口返回信息会展示在这里。</div>
                  </div>
                  <div class="tool-shell__result-tag">BindCard Output</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input
                      type="textarea"
                      :autosize="{minRows:8,maxRows:300}"
                      placeholder="绑卡结果"
                      v-model="resultText"
                      style="width: 100%"
                  />
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
            bindScene: 'DRAW',
            payChannel: 'baofu',
            cardNo: '',
            resultText: '',
            submitting: false,
            payChannelOptions: PAY_CHANNEL_OPTIONS,
        };
    },
    computed: {
        isAutoCardChannel() {
            return ['all', 'allinpay', 'huifu'].includes(this.payChannel);
        },
    },
    methods: {
        handlePayChannelChange(value) {
            if (['all', 'allinpay', 'huifu'].includes(value)) {
                this.cardNo = '';
            }
        },
        async submitBindCard() {
            if (!this.mobile) {
                this.$message.error('手机号必填');
                return;
            }
            if (this.submitting) {
                return;
            }

            this.submitting = true;
            this.resultText = `====绑卡提交中：${this.mobile}，场景=${this.bindScene}，通道=${this.payChannel}，勿重复点击====`;

            const payload = {
                env: this.selectedEnv,
                mobile: this.mobile,
                bindScene: this.bindScene,
                payChannel: this.payChannel,
                cardNo: this.isAutoCardChannel ? null : (this.cardNo || null),
            };

            try {
                const response = await fetch('api/h5/scene/bind_card', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                this.resultText = JSON.stringify(result, null, 2);
            } catch (e) {
                this.resultText = `请求异常: ${e}`;
            } finally {
                this.submitting = false;
            }
        }
    },
    mounted() {
        injectToolShellStyles();
    }
}
