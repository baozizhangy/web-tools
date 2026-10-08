import { callApi } from "../api/http.js";
export default {
  name: 'risk-input',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
  <div>
    <!-- 系统模块 -->
    <el-form-item label="系统模块：" class="risk-input-box">
      <el-autocomplete
        v-model="riskParam.selectedRiskModule"
        placeholder="系统模块"
      />
    </el-form-item>

    <!-- 业务类型 -->
    <el-form-item label="业务类型：" class="risk-input-box">
      <el-autocomplete
        v-model="riskParam.selectedRiskBizType"
        placeholder="业务类型"
        :value-key="'value'"
      />
    </el-form-item>

    <!-- 规则集 -->
    <el-form-item label="规则集：" class="risk-input-box">
      <el-autocomplete
        v-model="riskParam.selectedRuleSetNo"
        placeholder="规则集"
        :value-key="'value'"
      />
    </el-form-item>

    <!-- 三方资信 -->
    <el-form-item label="三方资信：" class="risk-input-box">
      <el-autocomplete
        v-model="riskParam.selectedIntfType"
        placeholder="选择被测三方资信"
        :value-key="'intfValue'"
        :props="{ label: 'intfName' }"
      />
    </el-form-item>

    <!-- 业务编号 -->
    <el-form-item label="业务编号：" class="risk-input-box">
      <el-input
        v-model="riskParam.riskBizNo"
        placeholder="业务编号"
      />
    </el-form-item>

    <!-- 是否返回预期数据 -->
    <el-form-item label="是否返回预期数据：" class="risk-input-box">
      <el-select v-model="riskParam.isReturnExpect" placeholder="选择是否返回预期数据">
        <el-option label="是" value="1" />
        <el-option label="否" value="0" />
      </el-select>
    </el-form-item>

    <!-- 操作按钮 -->
    <el-form-item>
      <el-button type="primary" @click="resetRiskParam">重置</el-button>
      <el-button
        type="primary"
        @click="riskInputCompare().then((r) => console.log(r))"
      >
        输入项校验
      </el-button>
    </el-form-item>

    <!-- widek平台admin-token -->
    <el-form-item label="widek平台admin-token：" class="risk-input-box">
      <el-input
        v-model="riskParam.widekAdminToken"
        placeholder="非必填，接口返回token失效时填写..."
        type="textarea"
      />
    </el-form-item>

    <!-- 执行结果 -->
    <el-form-item label="执行结果：" class="risk-input-box">
      <el-input
        ref="compareInputTextarea"
        v-model="riskParam.riskRes"
        type="textarea"
        placeholder="资信输入项对比结果"
        @input="adjustTextareaHeight('compareInputTextarea')"
      />
    </el-form-item>
  </div>
  `,
  data() {
    return {
      riskParam: {
        riskModuleList: ["TDS", "APV", "LPS"],
        riskBizTypeList: ["DIST"],
        ruleSetNoList: ["TDS-101", "TDS-301"],
        intfTypeList: [
          { "intfValue": "BrSpecial", "intfName": "百融-特殊名单BrSpecial" },
          { "intfValue": "BrHxStrategy", "intfName": "百融-借贷意向BrHxStrategy" },
          { "intfValue": "TcCreditProbe", "intfName": "天创-信用司南TcCreditProbe" },
          { "intfValue": "QCloudAntiFraud", "intfName": "QCloudAntiFraud" },
          { "intfValue": "TcScore", "intfName": "天创-信用分TcScore" },
          { "intfValue": "AliAntiFraudRisks", "intfName": "AliAntiFraudRisks" },
          { "intfValue": "AliAntiFraudV5", "intfName": "AliAntiFraudV5" },
          { "intfValue": "TcCreditMix", "intfName": "天创-TcCreditMix" },
          { "intfValue": "TcFireCloudScore", "intfName": "天创-火云分TcFireCloudScore" },
          { "intfValue": "XrModelScore137", "intfName": "XrModelScore137" }
        ],
        riskBizNo: '202405210000000006',
        widekAdminToken: '',
        selectedRiskModule: "TDS",
        selectedRiskBizType: "DIST",
        selectedRuleSetNo: "TDS-301",
        selectedIntfType: "BrHxStrategy",
        riskRes: "------------",
        isReturnExpect: "0"
      },
    };
  },
  computed: {
  },
  methods: {
    // 调用输入项对比
    async riskInputCompare() {
        const params = {
            env: this.selectedEnv,
            module: this.riskParam.selectedRiskModule,
            bizType: this.riskParam.selectedRiskBizType,
            ruleSetNo: this.riskParam.selectedRuleSetNo,
            intfType: this.riskParam.selectedIntfType,
            riskBizNo: this.riskParam.riskBizNo,
            widekAdminToken: this.riskParam.widekAdminToken,
            isReturnExpect: this.riskParam.isReturnExpect
        };
        this.riskParam.riskRes = '执行对比输入项中：{}'.replace("{}", JSON.stringify(params));
        console.log("riskParam", params);
        const response = await callApi("api/risk/input_compare", params)
        console.log("clearCache:response", response);
        this.riskParam.riskRes = JSON.stringify(response, null, 2);
    },
    // 重置风险参数
    resetRiskParam() {
                this.riskParam.selectedRiskModule = null;
                this.riskParam.selectedRiskBizType = null;
                this.riskParam.selectedRuleSetNo = null;
                this.riskParam.selectedIntfType = null;
                this.riskParam.riskBizNo = '';
            },
  },
}
