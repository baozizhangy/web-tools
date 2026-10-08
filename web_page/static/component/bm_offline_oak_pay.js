/**
 * 橡树线下还款组件
 * 
 * 功能说明:
 * - 通过 oakPayOrder 接口发起线下还款
 * - 自动执行线下还款批次处理 job
 * - 轮询验证当期是否结清
 * 
 * 使用场景:
 * - 部分成功状态需要线下还款完成当期结清
 * - 手动触发线下还款流程
 */

import {injectToolShellStyles} from './common/uiShell.js';

export default {
    name: 'offline-oak-pay',
    props: {
        // 当前选择的环境 (BM_SIT/DEV)
        selectedEnv: {
            type: String,
            required: true
        },
    },
    template: `
      <div class="tool-shell">
        <el-card shadow="hover" class="tool-shell__card tool-shell__card--compact">
          <div class="tool-shell__inner tool-shell__inner--compact">
            <!-- 页面头部 -->
            <div class="tool-shell__hero tool-shell__hero--teal tool-shell__hero--compact">
              <div class="tool-shell__hero-content">
                <div>
                  <div class="tool-shell__eyebrow">OFFLINE OAK PAY</div>
                  <div class="tool-shell__title">橡树线下还款</div>
                  <div class="tool-shell__desc">通过 oakPayOrder 接口发起线下还款，自动完成批次处理和结清验证</div>
                </div>
                <div class="tool-shell__stats">
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前环境</div>
                    <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                  </div>
                  <div class="tool-shell__stat">
                    <div class="tool-shell__stat-label">当前方法</div>
                    <div class="tool-shell__stat-value">offline_oak_pay_order</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="tool-shell__compact-grid">
              <!-- 表单区域 -->
              <div class="tool-shell__panel tool-shell__panel--soft tool-shell__panel--compact">
                <div class="tool-shell__panel-head">
                  <div>
                    <div class="tool-shell__panel-title">还款参数</div>
                    <div class="tool-shell__panel-desc">请输入手机号、借据号和期数，系统将自动执行线下还款流程。</div>
                  </div>
                  <div class="tool-shell__method-pill">OAK PAY</div>
                </div>

                <el-form label-position="top" class="tool-shell__compact-form">
                  <!-- 第一行：手机号和借据号 -->
                  <div class="tool-shell__compact-fields tool-shell__compact-fields--two">
                    <el-form-item label="手机号">
                      <el-input
                          v-model="mobile"
                          placeholder="请输入手机号"
                          clearable
                      />
                    </el-form-item>
                    <el-form-item label="借据号">
                      <el-input
                          v-model="loanNo"
                          placeholder="请输入借据号 LNxxxx"
                          clearable
                      />
                    </el-form-item>
                  </div>
                  
                  <!-- 第二行：期数 -->
                  <div class="tool-shell__compact-fields tool-shell__compact-fields--single">
                    <el-form-item label="还款期数">
                      <el-select
                          v-model="terms"
                          placeholder="请选择还款期数"
                          style="width: 100%"
                      >
                        <el-option
                            v-for="item in termsOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                      </el-select>
                    </el-form-item>
                  </div>
                  
                  <!-- 提交按钮 -->
                  <div class="tool-shell__actions">
                    <el-button
                        class="tool-shell__primary-btn"
                        @click="executeOfflineOakPay"
                        :loading="isExecuting"
                        :disabled="isExecuting"
                        type="primary"
                    >
                      执行线下还款
                    </el-button>
                  </div>
                </el-form>
              </div>

              <!-- 结果展示区域 -->
              <div class="tool-shell__result tool-shell__result--compact">
                <div class="tool-shell__result-head">
                  <div>
                    <div class="tool-shell__result-title">执行日志</div>
                    <div class="tool-shell__result-desc">线下还款流程实时输出</div>
                  </div>
                  <div class="tool-shell__result-tag">Process Log</div>
                </div>
                <div class="tool-shell__result-body">
                  <el-input
                      type="textarea"
                      :autosize="{minRows:8,maxRows:300}"
                      placeholder="线下还款流程日志将在此显示"
                      v-model="resultInfo"
                      style="width: 100%">
                  </el-input>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    `,
    data() {
        return {
            // 表单字段
            mobile: '',           // 手机号
            loanNo: '',          // 借据号
            terms: '',           // 期数
            
            // 期数选项 (1-12期)
            termsOptions: [
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
            
            // 执行状态
            isExecuting: false,   // 是否正在执行
            resultInfo: '',       // 结果日志
        }
    },
    mounted() {
        // 注入样式
        injectToolShellStyles();
    },
    methods: {
        /**
         * 执行线下还款
         * 
         * 流程说明:
         * 1. 校验必填参数
         * 2. 发起 POST 请求到后端接口
         * 3. 通过 SSE 流式接收执行日志
         * 4. 显示最终执行结果
         */
        executeOfflineOakPay() {
            // 参数校验
            if (!this.mobile) {
                ElementPlus.ElMessage.error('请输入手机号');
                return;
            }
            if (!this.loanNo) {
                ElementPlus.ElMessage.error('请输入借据号');
                return;
            }
            if (!this.terms) {
                ElementPlus.ElMessage.error('请选择还款期数');
                return;
            }

            // 重置状态
            this.isExecuting = true;
            this.resultInfo = '';

            // 发起 POST 请求
            fetch('/api/offline_oak_pay', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    mobile: this.mobile,
                    loan_no: this.loanNo,
                    terms: this.terms,
                    env: this.selectedEnv
                })
            }).then(response => {
                // 获取流式响应的 reader
                const reader = response.body.getReader();
                const decoder = new TextDecoder();

                /**
                 * 处理流式数据
                 * 
                 * SSE 数据格式:
                 * data: {"type": "progress", "message": "..."}
                 * data: {"type": "done", "result": {...}}
                 * data: {"type": "error", "message": "..."}
                 */
                const processStream = ({done, value}) => {
                    if (done) {
                        this.isExecuting = false;
                        return;
                    }

                    // 解码数据块
                    const chunk = decoder.decode(value, {stream: true});
                    const lines = chunk.split('\n');

                    // 处理每一行数据
                    lines.forEach(line => {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.substring(6));
                                
                                // 处理进度消息
                                if (data.type === 'progress') {
                                    this.resultInfo += data.message + '\n';
                                } 
                                // 处理完成消息
                                else if (data.type === 'done') {
                                    this.resultInfo += '\n========== 执行完成 ==========\n';
                                    const result = data.result;
                                    
                                    if (result.success) {
                                        this.resultInfo += `结果: ${result.message}\n`;
                                        this.resultInfo += `借据号: ${result.loanNo}\n`;
                                        this.resultInfo += `期数: ${result.terms}\n`;
                                        this.resultInfo += `金额: ${result.totalAmount}\n`;
                                        ElementPlus.ElMessage.success('线下还款成功');
                                    } else {
                                        this.resultInfo += `错误: ${result.message}\n`;
                                        this.resultInfo += `错误码: ${result.code}\n`;
                                        ElementPlus.ElMessage.error('线下还款失败');
                                    }
                                    
                                    this.isExecuting = false;
                                } 
                                // 处理错误消息
                                else if (data.type === 'error') {
                                    this.resultInfo += '\n========== 执行异常 ==========\n';
                                    this.resultInfo += `错误: ${data.message}\n`;
                                    this.isExecuting = false;
                                    ElementPlus.ElMessage.error('线下还款异常');
                                }
                            } catch (e) {
                                console.error('解析SSE数据失败:', e, line);
                            }
                        }
                    });

                    // 继续读取下一块数据
                    return reader.read().then(processStream);
                };

                // 开始读取流
                return reader.read().then(processStream);
            }).catch(error => {
                // 处理网络错误
                console.error('请求错误:', error);
                this.resultInfo += '\n========== 连接异常 ==========\n';
                this.resultInfo += `错误: ${error.message}\n`;
                this.isExecuting = false;
                ElementPlus.ElMessage.error('连接异常，请重试');
            });
        }
    }
}
