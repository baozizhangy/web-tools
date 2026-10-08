import {callApi} from '../api/http.js'
import { injectToolShellStyles } from './common/uiShell.js';

export default {
    name: 'update-mock',
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
            <div class="tool-shell__hero tool-shell__hero--teal">
              <div class="tool-shell__hero-content">
                <div>
                  <div class="tool-shell__eyebrow">MOCK SCHEDULE</div>
                  <div class="tool-shell__title">mock还款计划调整</div>
                  <div class="tool-shell__desc">修改金额期数，账单日格式为yyyy-mm-dd</div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">资方选择</div>
                    <div class="tool-shell__stat-value">{{ selectFund || '未选择' }}</div>
                  </div>
                </div>
              </div>
            </div>

            <el-form label-position="top">
              <div class="tool-shell__panel tool-shell__panel--soft">
                <div class="tool-shell__panel-title">修改参数</div>
                <div class="tool-shell__panel-desc">选择资方、期数并填写金额和账单日</div>
                <el-row :gutter="20">
                  <el-col :xs="24" :md="12">
                    <el-form-item label="选择修改资方">
                      <el-select v-model="selectFund" placeholder="选择资方" style="width: 100%">
                        <el-option
                            v-for="option in fundCodes"
                            :key="option.value"
                            :label="option.value"
                            :value="option.value"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="12">
                    <el-form-item label="选择修改期数">
                      <el-select v-model="selectItem" placeholder="请选择类型" style="width: 100%">
                        <el-option
                            v-for="option in mockItems"
                            :key="option.value"
                            :label="option.label"
                            :value="option.value"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :xs="24" :md="12">
                    <el-form-item label="输入金额">
                      <el-input
                          v-model="amt"
                          class="input_box"
                          type="text"
                          placeholder="还款计划本金"
                          clearable
                          style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="12">
                    <el-form-item label="输入账单日">
                      <el-input
                          v-model="is_date"
                          class="input_box"
                          type="text"
                          placeholder="第一期账单日"
                          clearable
                          style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-form-item label="客户号" v-if="selectFund === 'ALLINSUSHANG'">
                  <el-input
                      v-model="cust_no"
                      placeholder="请输入cust_no"
                      clearable
                      style="width: 100%"
                  />
                </el-form-item>

                <div class="tool-shell__tip tool-shell__tip--teal">苏商资方要求 cust_no 必填</div>

                <div class="tool-shell__actions">
                  <el-button id="submitCreditBtn" @click="UpdateData" type="primary" class="tool-shell__primary-btn tool-shell__primary-btn--teal">
                    提交修改
                  </el-button>
                </div>
              </div>

              <div class="tool-shell__result tool-shell__result--teal">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">修改结果</div>
                    <div class="tool-shell__result-desc">查看 mock 修改执行结果和失败原因。</div>
                  </div>
                  <div class="tool-shell__result-tag">Mock Output</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input
                      type="textarea"
                      placeholder="mock修改结果"
                      v-model="mock_update_info"
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
            amt: '',
            selectItem: null,
            selectFund: null,
            cust_no: '',
            is_date: '',
            mock_update_info: '',
            fundCodes: [
                {
                    label: '众邦',
                    value: 'ZBANK_F8',
                    title: '众邦',
                },
                {
                    label: '苏商',
                    value: 'ALLINSUSHANG',
                    title: '苏商',
                },
                {
                    label: '蓝海',
                    value: 'ALLINBLUEOCEAN',
                    title: '蓝海',
                },
                {
                    label: '中黔联',
                    value: 'ZHONGQIANLIAN',
                    title: '中黔联',
                },
            ],
            mockItems: [
                {
                    label: '3',
                    value: 3,
                    title: '3期'
                },
                {
                    label: '6',
                    value: 6,
                    title: '6期'
                },
                {
                    label: '9',
                    value: 9,
                    title: '9期'
                },
                {
                    label: '12',
                    value: 12,
                    title: '12期'
                },
            ]
        }
    },
    methods: {
        async UpdateData() {
            if (!this.amt || !this.selectItem || !this.selectFund) {
                alert('期数、资方、金额不能为空');
                return;
            }

            if (this.selectFund === 'ALLINSUSHANG' && !this.cust_no) {
                alert('ALLINSUSHANG 资方需要填写客户号');
                return;
            }
            const data = {
                env: this.selectedEnv,
                amt: this.amt,
                fund_code: this.selectFund,
                period: this.selectItem,
                is_date: this.is_date
            }
            if (this.selectFund === 'ALLINSUSHANG') {
                data.cust_no = this.cust_no;
            }
            let update_url = 'api/bm_update_mock';

            const response = await fetch(update_url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            console.log('查询借据状态返回结果', response.ok)
            if (response.ok) {
                const result = await response.json();
                let message_info = '';
                if (result.success === 0) {
                    message_info = 'mock数据修改成功' + result.res;
                    alert('{}mock数据修改成功'.replace('{}', this.selectFund))
                } else if (result.success === 1) {
                    message_info = 'mock数据修改失败，请检查提交数据' + result.res;
                } else if (result.success === 2) {
                    message_info = 'is_date传值错误，检查数据后重新提交' + result.res;
                } else {
                    throw new Error(`${response.status} ${response.statusText}`);
                }
                this.mock_update_info += '\n' + message_info + '\n';
            } else {
                console.error('请求失败:', response.status, response.statusText);
                alert('请求失败，请稍后再试');
            }
        }
    },
    mounted() {
        injectToolShellStyles();
    }
}
