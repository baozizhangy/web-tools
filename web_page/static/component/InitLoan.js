import {injectToolShellStyles} from './common/uiShell.js';

export default {
    name: 'init-loan',
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
            <div class="tool-shell__hero tool-shell__hero--amber tool-shell__hero--compact">
              <div class="tool-shell__hero-content">
                <div>
                  <div class="tool-shell__eyebrow">LOAN WORKFLOW</div>
                  <div class="tool-shell__title">借据调试工作台</div>
                  <div class="tool-shell__desc">
                    把多个方法收进一个入口里，通过顶部切换快速切面，减少表单堆叠，提升联调效率。
                  </div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前方法</div>
                    <div class="tool-shell__stat-value">{{ activeMethodLabel }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="tool-shell__compact-tabs">
              <button
                  v-for="method in methodTabs"
                  :key="method.value"
                  type="button"
                  class="tool-shell__compact-tab"
                  :class="{'tool-shell__compact-tab--active': activeMethod === method.value}"
                  @click="activeMethod = method.value"
              >
                <span class="tool-shell__compact-tab-title">{{ method.label }}</span>
                <span class="tool-shell__compact-tab-desc">{{ method.title }}</span>
              </button>
            </div>

            <div class="tool-shell__compact-grid">
              <div class="tool-shell__panel tool-shell__panel--soft tool-shell__panel--compact">
                <div class="tool-shell__panel-head">
                  <div>
                    <div class="tool-shell__panel-title">{{ activeMethodLabel }}</div>
                    <div class="tool-shell__panel-desc">{{ activeMethodDesc }}</div>
                  </div>
                  <div class="tool-shell__method-pill">{{ activeMethodTag }}</div>
                </div>

                <el-form v-if="activeMethod === 'init_bill'" label-position="top" class="tool-shell__compact-form">
                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item label="借据单号">
                      <el-input class="input_box" type="text" v-model="Loan_no" placeholder="助贷内 loan_no" clearable/>
                    </el-form-item>
                    <el-form-item label="借据状态">
                      <el-select v-model="overdueType" placeholder="请选择借据状态" style="width: 100%">
                        <el-option label="不逾期" value="N"/>
                        <el-option label="逾期" value="Y"/>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item v-if="overdueType === 'N'" label="选择初始化后状态">
                      <el-radio-group v-model="billDayMode">
                        <el-radio label="bill_day">账单日</el-radio>
                        <el-radio label="custom_day">计息天数</el-radio>
                      </el-radio-group>
                    </el-form-item>
                    <el-form-item :label="overdueType === 'Y' ? '逾期天数' : '计息天数'">
                      <el-input class="input_box" type="number" v-model="day"
                                :placeholder="overdueType === 'Y' ? '请输入逾期天数' : '请输入计息计费天数'" clearable
                                :disabled="overdueType === 'N' && billDayMode === 'bill_day'"/>
                    </el-form-item>
                  </div>
                  <div class="tool-shell__tip">
                    逾期：填写需要的逾期天数；非逾期：直接填写第一期需要计息计费几天，选择账单日则初始化到第一期支持正常还款。
                  </div>
                  <div class="tool-shell__actions tool-shell__actions--compact">
                    <el-button class="tool-shell__primary-btn" @click="InitLoan" type="primary">执行初始化</el-button>
                  </div>
                </el-form>

                <el-form v-else label-position="top" class="tool-shell__compact-form">
                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item label="借据单号">
                      <el-input class="input_box" type="text" v-model="compensationLoanNo" placeholder="助贷内 loan_no"
                                clearable/>
                    </el-form-item>
                    <el-form-item label="资方编码">
                      <el-select v-model="compensationFundCode" placeholder="请选择资方" style="width: 100%" clearable>
                        <el-option v-for="option in compensationFundCodes" :key="option.value" :label="option.label"
                                   :value="option.value"/>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div class="tool-shell__compact-fields tool-shell__compact-fields--single">
                    <el-form-item label="代偿几期">
                      <el-input class="input_box" type="number" v-model="compensationNumber"
                                placeholder="需要回购可不填写" clearable/>
                    </el-form-item>
                  </div>
                  <div class="tool-shell__tip tool-shell__tip--teal">
                    填入需要代偿的期数；超过连三累六配置时会按资方规则走回购，整体耗时会更长。
                  </div>
                  <div class="tool-shell__actions tool-shell__actions--compact">
                    <el-button class="tool-shell__primary-btn tool-shell__primary-btn--teal" @click="CompensateLoan"
                               type="primary">执行代偿
                    </el-button>
                  </div>
                </el-form>
              </div>

              <div class="tool-shell__result tool-shell__result--teal tool-shell__result--compact">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">执行日志</div>
                    <div class="tool-shell__result-desc">统一查看当前方法的执行结果与关键输出。</div>
                  </div>
                  <div class="tool-shell__result-tag">{{ activeMethodTag }}</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input type="textarea" :autosize="{minRows:14,maxRows:320}"
                            placeholder="执行过程与返回结果会显示在这里" v-model="init_loan_info"></el-input>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    `,
    data() {
        return {
            activeMethod: 'init_bill',
            Loan_no: '',
            overdueType: 'N',
            day: '',
            billDayMode: 'bill_day',
            compensationLoanNo: '',
            compensationFundCode: '',
            compensationNumber: '',
            init_loan_info: '',
            methodTabs: [
                {
                    label: '借据初始化',
                    value: 'init_bill',
                    title: '支持逾期、非逾期与账单日模式',
                    tag: 'INIT',
                    desc: '调整账单初始化日期与逾期参数，快速恢复到目标账单状态。'
                },
                {
                    label: '借据代偿',
                    value: 'loan_compensation',
                    title: '按资方配置自动代偿 / 回购',
                    tag: 'COMP',
                    desc: '自动计算有效期次和初始化逾期天数，等待账单到位后循环触发代偿。'
                },
            ],
            compensationFundCodes: [
                {label: '众邦', value: 'ZBANK_E8', title: '众邦'},
                {label: '苏商', value: 'ALLINSUSHANG_F24', title: '苏商'},
                {label: '蓝海', value: 'ALLINBLUEOCEAN_F24', title: '蓝海'},
                {label: '中黔联', value: 'ZHONGQIANLIAN_F36', title: '中黔联'},
            ]
        }
    },
    computed: {
        activeMethodMeta() {
            return this.methodTabs.find(item => item.value === this.activeMethod) || this.methodTabs[0];
        },
        activeMethodLabel() {
            return this.activeMethodMeta.label;
        },
        activeMethodDesc() {
            return this.activeMethodMeta.desc;
        },
        activeMethodTag() {
            return this.activeMethodMeta.tag;
        }
    },
    methods: {
        async InitLoan() {
            this.init_loan_info = `====初始化借据：${this.Loan_no}，勿重复点击====`;
            const data = {
                loan_no: this.Loan_no,
                overdue_type: this.overdueType,
                day: this.overdueType === 'N' && this.billDayMode === 'bill_day' ? 0 : this.day,
                bill_day: this.overdueType === 'N' ? this.billDayMode === 'bill_day' : false,
                env: this.selectedEnv,
            };
            if (!data.loan_no) return alert('缺少必填参数');
            if (data.overdue_type === 'Y' && (data.day === '' || data.day === null || data.day === undefined)) return alert('缺少逾期天数');
            if (data.overdue_type === 'N' && !data.bill_day && (data.day === '' || data.day === null || data.day === undefined)) return alert('缺少计息天数');
            try {
                const response = await fetch('api/init_plan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    const result = await response.json();
                    let messageInfo = '';
                    if (result.success === 0) messageInfo = '借据初始化成功，请查看借据详情';
                    else if (result.success === 1) {
                        messageInfo = '试算接口超时，检查计息，或手动触发计息或重试';
                        alert('试算超时');
                    } else messageInfo = result.res || '借据初始化失败，请检查提交数据，手动触发计息或重试';
                    this.init_loan_info += `
${messageInfo}
`;
                }
            } catch (error) {
                console.error('请求出错:', error);
                alert('请求出错，请检查网络连接');
            }
        },
        async CompensateLoan() {
            const data = {
                loan_no: this.compensationLoanNo,
                fund_code: this.compensationFundCode,
                number: this.compensationNumber === '' ? null : this.compensationNumber,
                env: this.selectedEnv
            };
            if (!data.loan_no) return alert('缺少 loan_no');
            if (!data.fund_code) return alert('缺少 fund_code');
            this.init_loan_info = `====执行代偿：${data.loan_no}，测试环境执行较慢预计两分钟====`;
            
            try {
                const response = await fetch('api/loan_compensation', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    const result = await response.json();
                    if (result.success === 0) {
                        const summary = result.data || {};
                        this.init_loan_info += `${result.res}`;
                        this.init_loan_info += `资方: ${summary.fund_code || data.fund_code}`;
                        this.init_loan_info += `执行期次: ${summary.effective_number ?? '--'}`;
                        this.init_loan_info += `初始化逾期天数: ${summary.max_day ?? '--'}
`;
                    } else {
                        this.init_loan_info += `
${result.res || '代偿流程执行失败'}
`;
                        alert(result.res || '代偿流程执行失败');
                    }
                }
            } catch (error) {
                console.error('请求出错:', error);
                alert('请求出错，请检查网络连接');
            }
        },
    },
    mounted() {
        injectToolShellStyles();
    }
}
