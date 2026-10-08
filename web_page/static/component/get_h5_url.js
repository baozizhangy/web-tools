import { injectToolShellStyles } from './common/uiShell.js';

export default {
    name: 'get-url',
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
                  <div class="tool-shell__eyebrow">H5 ENTRY</div>
                  <div class="tool-shell__title">H5 链接工作台</div>
                  <div class="tool-shell__desc">沿用紧凑模块布局，场景仍通过下拉框选择，方便保持现有使用习惯。</div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前场景</div>
                    <div class="tool-shell__stat-value">{{ selectUrlItem || '未选择' }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="tool-shell__compact-grid">
              <div class="tool-shell__panel tool-shell__panel--soft tool-shell__panel--compact">
                <div class="tool-shell__panel-head">
                  <div>
                    <div class="tool-shell__panel-title">链接参数</div>
                    <div class="tool-shell__panel-desc">输入手机号并通过下拉选择借款或还款场景，获取对应 H5 链接。</div>
                  </div>
                  <div class="tool-shell__method-pill">LINK</div>
                </div>

                <el-form label-position="top" class="tool-shell__compact-form">
                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
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
                    <el-form-item label="选择节点">
                      <el-select v-model="selectUrlItem" placeholder="选择节点" style="width: 100%">
                        <el-option
                            v-for="option in UrlItems"
                            :key="option.value"
                            :label="option.label"
                            :value="option.value"
                        />
                      </el-select>
                    </el-form-item>
                  </div>

                  <div class="tool-shell__tip">当前不启用顶部场景切换，继续使用下拉框选择借款或还款。</div>
                  <div class="tool-shell__actions tool-shell__actions--compact">
                    <el-button class="tool-shell__primary-btn" @click="GetUrl" type="primary">
                      获取H5链接
                    </el-button>
                  </div>
                </el-form>
              </div>

              <div class="tool-shell__result tool-shell__result--compact">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">URL 信息</div>
                    <div class="tool-shell__result-desc">接口返回的链接或错误信息会展示在这里。</div>
                  </div>
                  <div class="tool-shell__result-tag">Link Output</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input
                      type="textarea"
                      v-model="get_url_info"
                      placeholder="接口返回信息"
                      :autosize="{minRows:14,maxRows:320}"
                      readonly
                      style="width: 100%;"
                  />
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    `,
    data() {
        return {
            selectUrlItem: null,
            get_url_info: '',
            Mobile: '',
            UrlItems: [
                {
                    value: 'DRAW',
                    label: '借款',
                },
                {
                    value: 'REPAY',
                    label: '还款',
                },
            ],
        }
    },
    methods: {
        async GetUrl() {
            if (!this.selectUrlItem) {
                this.$alert('请选择H5链接节点！');
                return;
            }
            const data = {
                mobile: this.Mobile,
                env: this.selectedEnv,
                scene: this.selectUrlItem,
            }
            const response = await fetch('api/bm_get_h5_url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                let message_info = '';
                if (result.success === 0 || result.success === -1) {
                    message_info = typeof result.res === 'object'
                        ? JSON.stringify(result.res, null, 2)
                        : result.res;
                }
                this.get_url_info += '\n' + message_info + '\n';
            } else {
                this.get_url_info += '请求失败，请稍后再试';
                alert('请求失败，请稍后再试')
            }
        },
    },
    mounted() { injectToolShellStyles(); }
}
