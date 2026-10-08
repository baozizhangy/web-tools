import { injectToolShellStyles } from './common/uiShell.js';

export default {
    name: 'h5-draw-submit',
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
                  <div class="tool-shell__eyebrow">H5 DRAW SCENE</div>
                  <div class="tool-shell__title">H5 借款申请</div>
                  <div class="tool-shell__desc">保持单流程交互，只将页面收敛到更紧凑的输入区与结果区布局。</div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">权益购买</div>
                    <div class="tool-shell__stat-value">{{ isPrivilegeProcess }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="tool-shell__compact-grid">
              <div class="tool-shell__panel tool-shell__panel--soft tool-shell__panel--compact">
                <div class="tool-shell__panel-head">
                  <div>
                    <div class="tool-shell__panel-title">借款参数</div>
                    <div class="tool-shell__panel-desc">手机号必填，金额范围 1000~10000，期数仅支持 3/6/9/12。</div>
                  </div>
                  <div class="tool-shell__method-pill">DRAW</div>
                </div>

                <el-form label-position="top" class="tool-shell__compact-form">
                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item label="手机号（必填）">
                      <el-input v-model.trim="mobile" class="input_box" type="text" placeholder="请输入手机号" clearable style="width: 100%" />
                    </el-form-item>
                    <el-form-item label="借款金额">
                      <el-input v-model.trim="amt" class="input_box" type="text" placeholder="1000 ~ 10000" clearable style="width: 100%" />
                    </el-form-item>
                  </div>

                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item label="借款期数">
                      <el-select v-model="term" style="width: 100%" placeholder="请选择期数">
                        <el-option label="3" :value="3" />
                        <el-option label="6" :value="6" />
                        <el-option label="9" :value="9" />
                        <el-option label="12" :value="12" />
                      </el-select>
                    </el-form-item>
                    <el-form-item label="是否购买权益">
                      <el-select v-model="isPrivilegeProcess" style="width: 100%" placeholder="请选择">
                        <el-option label="N - 不购买" value="N" />
                        <el-option label="Y - 购买" value="Y" />
                      </el-select>
                    </el-form-item>
                  </div>

                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item label="是否连续包月" v-if="isPrivilegeProcess === 'Y'">
                      <el-select v-model="isContinuousMonthly" style="width: 100%" placeholder="请选择">
                        <el-option label="Y - 连续包月（OM）" value="Y" />
                        <el-option label="N - 单月（CM）" value="N" />
                      </el-select>
                    </el-form-item>
                    <el-form-item label="借款用途描述">
                      <el-input v-model.trim="loanPurposeDesc" class="input_box" type="text" placeholder="默认：购物" clearable style="width: 100%" />
                    </el-form-item>
                  </div>

                  <div class="tool-shell__compact-fields tool-shell__compact-fields--single">
                    <el-form-item label="借款用途编码">
                      <el-input v-model.trim="loanPurposeCode" class="input_box" type="text" placeholder="默认：01" clearable style="width: 100%" />
                    </el-form-item>
                  </div>

                  <div class="tool-shell__actions tool-shell__actions--compact">
                    <el-button class="tool-shell__primary-btn" type="primary" @click="submitDraw" :loading="submitting">提交 H5 借款</el-button>
                  </div>
                </el-form>
              </div>

              <div class="tool-shell__result tool-shell__result--compact">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">返回结果</div>
                    <div class="tool-shell__result-desc">先展示关键步骤，再展示完整返回结果。</div>
                  </div>
                  <div class="tool-shell__result-tag">Draw Output</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input type="textarea" :autosize="{minRows:14,maxRows:320}" placeholder="借款场景返回结果" v-model="resultText" style="width: 100%" />
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    `,
    data() {
        return {
            mobile: '',
            amt: '3000',
            term: 12,
            isPrivilegeProcess: 'N',
            isContinuousMonthly: 'Y',
            loanPurposeDesc: '购物',
            loanPurposeCode: '01',
            resultText: '',
            submitting: false,
        };
    },
    methods: {
        async submitDraw() {
            if (!this.mobile) return this.$message.error('手机号必填');
            if (!this.amt || !this.term) return this.$message.error('金额和期数必填');
            if (this.submitting) return;

            this.submitting = true;
            this.resultText = `====H5 借款提交中：${this.mobile}，勿重复点击====`;
            const payload = {
                env: this.selectedEnv,
                mobile: this.mobile,
                amt: this.amt,
                term: this.term,
                isPrivilegeProcess: this.isPrivilegeProcess,
                isContinuousMonthly: this.isContinuousMonthly,
                loanPurposeDesc: this.loanPurposeDesc || '购物',
                loanPurposeCode: this.loanPurposeCode || '01',
            };

            try {
                const response = await fetch('api/h5/scene/draw_submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Accept': 'text/event-stream' },
                    body: JSON.stringify(payload)
                });
                if (!response.ok || !response.body) throw new Error(`请求失败: ${response.status}`);
                const reader = response.body.getReader();
                const decoder = new TextDecoder('utf-8');
                let buffer = '';
                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    buffer += decoder.decode(value, { stream: true });
                    const chunks = buffer.split('\n\n');
                    buffer = chunks.pop() || '';
                    for (const chunk of chunks) {
                        const line = chunk.split('\n').find(item => item.startsWith('data: '));
                        if (!line) continue;
                        const event = JSON.parse(line.slice(6));
                        if (event.type === 'progress') {
                            this.resultText += `${this.resultText ? '\n' : ''}[STEP] ${event.message}`;
                        } else if (event.type === 'done') {
                            this.resultText += `\n\n${JSON.stringify({ success: 0, data: event.result }, null, 2)}`;
                        } else if (event.type === 'error') {
                            this.resultText += `${this.resultText ? '\n' : ''}[ERROR] ${event.message}`;
                        }
                    }
                }
            } catch (e) {
                this.resultText = `请求异常: ${e}`;
            } finally {
                this.submitting = false;
            }
        }
    },
    mounted() { injectToolShellStyles(); }
};
