import { injectToolShellStyles } from './common/uiShell.js';

export default {
    name: 'h5-repay-scene',
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
                  <div class="tool-shell__eyebrow">H5 REPAY SCENE</div>
                  <div class="tool-shell__title">H5 还款工作台</div>
                  <div class="tool-shell__desc">支持还款场景与领取优惠券两类流程，通过分页切换操作。</div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前分页</div>
                    <div class="tool-shell__stat-value">{{ activeTabLabel }}</div>
                  </div>
                </div>
              </div>
            </div>

            <el-tabs v-model="activeTab" class="tool-shell__tabs">
              <el-tab-pane label="H5 还款场景" name="repay">
                <div class="tool-shell__compact-grid">
                  <div class="tool-shell__panel tool-shell__panel--soft tool-shell__panel--compact">
                    <div class="tool-shell__panel-head">
                      <div>
                        <div class="tool-shell__panel-title">还款参数</div>
                        <div class="tool-shell__panel-desc">输入手机号、借据号，并通过下拉框选择单期还款或提前结清。</div>
                      </div>
                      <div class="tool-shell__method-pill">REPAY</div>
                    </div>

                    <el-form label-position="top" class="tool-shell__compact-form">
                      <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                        <el-form-item label="手机号（必填）">
                          <el-input v-model.trim="mobile" class="input_box" type="text" placeholder="请输入手机号" clearable style="width: 100%" />
                        </el-form-item>
                        <el-form-item label="借据号（必填）">
                          <el-input v-model.trim="loanNo" class="input_box" type="text" placeholder="请输入借据号" clearable style="width: 100%" />
                        </el-form-item>
                      </div>
                      <div class="tool-shell__compact-fields tool-shell__compact-fields--single">
                        <el-form-item label="还款方式">
                          <el-select v-model="repayType" style="width: 100%" placeholder="请选择还款方式">
                            <el-option label="单期还款" value="SINGLE" />
                            <el-option label="提前结清" value="ALL" />
                          </el-select>
                        </el-form-item>
                      </div>
                      <div class="tool-shell__compact-fields tool-shell__compact-fields--single">
                        <el-form-item label="使用优惠券">
                          <el-switch v-model="useCoupon" active-text="使用优惠券还款" />
                        </el-form-item>
                      </div>
                      <div class="tool-shell__tip tool-shell__tip--teal">开启优惠券开关后，将使用 couponInfo 中返回的优惠券进行还款。</div>
                      <div class="tool-shell__actions tool-shell__actions--compact">
                        <el-button class="tool-shell__primary-btn tool-shell__primary-btn--teal" type="primary" @click="submitRepayScene" :loading="submitting">执行 H5 还款场景</el-button>
                      </div>
                    </el-form>
                  </div>

                  <div class="tool-shell__result tool-shell__result--teal tool-shell__result--compact">
                    <div class="tool-shell__result-head">
                      <div>
                        <div class="tool-shell__result-title">过程输出</div>
                        <div class="tool-shell__result-desc">实时展示步骤日志，并在完成后输出完整结果。</div>
                      </div>
                      <div class="tool-shell__result-tag">{{ repayTypeLabel }}</div>
                    </div>
                    <div class="tool-shell__result-body">
                      <el-input type="textarea" :autosize="{minRows:14,maxRows:320}" placeholder="H5 还款场景过程输出" v-model="resultText" style="width: 100%" />
                    </div>
                  </div>
                </div>
              </el-tab-pane>

              <el-tab-pane label="领取优惠券" name="coupon">
                <div class="tool-shell__compact-grid">
                  <div class="tool-shell__panel tool-shell__panel--soft tool-shell__panel--compact">
                    <div class="tool-shell__panel-head">
                      <div>
                        <div class="tool-shell__panel-title">领取优惠券</div>
                        <div class="tool-shell__panel-desc">填写手机号、user_no 和券类型后，执行保存并确认任务流程。</div>
                      </div>
                      <div class="tool-shell__method-pill">COUPON</div>
                    </div>

                    <el-form label-position="top" class="tool-shell__compact-form">
                      <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                        <el-form-item label="手机号（必填）">
                          <el-input v-model.trim="couponMobile" class="input_box" type="text" placeholder="请输入手机号" clearable style="width: 100%" />
                        </el-form-item>
                        <el-form-item label="user_no（必填）">
                          <el-input v-model.trim="couponUserNo" class="input_box" type="text" placeholder="请输入 user_no" clearable style="width: 100%" />
                        </el-form-item>
                      </div>
                      <div class="tool-shell__compact-fields tool-shell__compact-fields--single">
                        <el-form-item label="券类型（必填）">
                          <el-select v-model="couponType" style="width: 100%" placeholder="请选择券类型">
                            <el-option label="折扣券" value="discount" />
                            <el-option label="固定金额券" value="fixed" />
                          </el-select>
                        </el-form-item>
                      </div>
                      <div class="tool-shell__tip tool-shell__tip--teal">会自动更新模板 Excel、调用 save 接口，并继续提交确认任务。</div>
                      <div class="tool-shell__actions tool-shell__actions--compact">
                        <el-button class="tool-shell__primary-btn tool-shell__primary-btn--teal" type="primary" @click="submitCouponReceive" :loading="couponSubmitting">领取优惠券</el-button>
                      </div>
                    </el-form>
                  </div>

                  <div class="tool-shell__result tool-shell__result--teal tool-shell__result--compact">
                    <div class="tool-shell__result-head">
                      <div>
                        <div class="tool-shell__result-title">领取结果</div>
                        <div class="tool-shell__result-desc">展示保存任务与提交确认任务的返回结果。</div>
                      </div>
                      <div class="tool-shell__result-tag">COUPON</div>
                    </div>
                    <div class="tool-shell__result-body">
                      <el-input type="textarea" :autosize="{minRows:14,maxRows:320}" placeholder="领取优惠券结果输出" v-model="couponResultText" style="width: 100%" />
                    </div>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-card>
      </div>
    `,
    data() {
        return {
            activeTab: 'repay',
            mobile: '',
            loanNo: '',
            repayType: 'SINGLE',
            useCoupon: false,
            resultText: '',
            submitting: false,
            couponMobile: '',
            couponUserNo: '',
            couponType: '',
            couponResultText: '',
            couponSubmitting: false,
        };
    },
    computed: {
        repayTypeLabel() {
            return this.repayType === 'ALL' ? '提前结清' : '单期还款';
        },
        activeTabLabel() {
            return this.activeTab === 'coupon' ? '领取优惠券' : 'H5 还款场景';
        },
    },
    methods: {
        async submitRepayScene() {
            if (!this.mobile) return this.$message.error('手机号必填');
            if (!this.loanNo) return this.$message.error('借据号必填');
            if (this.submitting) return;

            this.submitting = true;
            this.resultText = `====H5 还款场景执行中：${this.loanNo}，勿重复点击====`;
            const payload = { env: this.selectedEnv, mobile: this.mobile, loanNo: this.loanNo, repayType: this.repayType, useCoupon: this.useCoupon };

            try {
                const response = await fetch('api/h5/scene/repay', {
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
        },
        async submitCouponReceive() {
            if (!this.couponMobile) return this.$message.error('手机号必填');
            if (!this.couponUserNo) return this.$message.error('user_no必填');
            if (!this.couponType) return this.$message.error('券类型必填');
            if (this.couponSubmitting) return;

            this.couponSubmitting = true;
            this.couponResultText = '====领取优惠券执行中，请勿重复点击====';
            const payload = {
                env: this.selectedEnv,
                mobile: this.couponMobile,
                user_no: this.couponUserNo,
                couponType: this.couponType,
            };

            try {
                const response = await fetch('api/h5/scene/coupon_receive', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                this.couponResultText = JSON.stringify(result, null, 2);
                if (result.error) {
                    this.$message.error(result.error);
                } else {
                    this.$message.success('领取优惠券流程执行完成');
                }
            } catch (e) {
                this.couponResultText = `请求异常: ${e}`;
            } finally {
                this.couponSubmitting = false;
            }
        }
    },
    mounted() { injectToolShellStyles(); }
};
