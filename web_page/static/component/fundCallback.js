import { callApi } from '../api/http.js'

export default {
  name: 'fund-callback',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
    <div>
      <div>
        <span class="demonstration">选择机构-方法：</span>
        <el-cascader v-model="fundData.selectedValue" :options="fundList"
          :props="{ expandTrigger: 'hover' }" filterable clearable @change="getFundCallBackData">
        </el-cascader>
        <el-button type="primary" title="提交"
          @click="pushFundRequest"><el-icon><Promotion /></el-icon>提交请求</el-button>
      </div>
      <br>
      <el-row>
        <el-col :span="13">
          <div class="grid-content bg-purple">
            <div style="display: flex; align-items: center;">
              <span style="width: 100px;">回调地址：</span>
              <el-input v-model="fundCallBackUrl" placeholder="机构回调地址"></el-input>
            </div>
            回调参数：
            <el-input type="textarea" autosize placeholder="机构回调参数" v-model="fundCallBackData">
            </el-input>
          </div>
        </el-col>
        <el-col :span="11">
          <div class="grid-content bg-purple-light"></div>
        </el-col>
      </el-row>
    </div>
  `,
  data() {
    return {
      fundList: [],
      fundData: {
        selectedValue: null
      },
      // 机构回调相关变量
      fundCallBackUrl: null,
      fundCallBackData: null,
    };
  },
  computed: {
    tableColumns() {
      return this.rawData.length > 0 ? Object.keys(this.rawData[0]) : [];
    },
    tableData() {
      return this.rawData;
    }
  },
  methods: {
    async getFundCallBackData(data) {
      console.log("getFundCallBackData:data", data);
      const params = {
        fund: this.fundData.selectedValue[0],
        method: this.fundData.selectedValue[1],
      };
      const result = await callApi("api/fund/method", params);
      console.log("getFundCallBackData:result", result);
      this.fundCallBackUrl = result.method_url;
      this.fundCallBackData = JSON.stringify(result.method_data, null, 2);
    },
    async pushFundRequest() {
      const params = {
        url: this.fundCallBackUrl,
        data: this.fundCallBackData,
      };
      const response = await callApi("api/fund/push", params);
      // 将返回结果用通知展示

      // let htmlMessage = '<textarea rows="3" style="width: 100%;">' + JSON.stringify(response) + '</textarea>'
      this.$notify({
        title: '提交回调返回',
        customClass: 'channel-notify',
        dangerouslyUseHTMLString: true,
        duration: 0,
        message: JSON.stringify(response)
      });
    },
  },
  mounted() {
    const initFund = () => {
        callApi("api/fund/init").then(r => {
            console.log("Response::api/fund/init::", r.data);
            this.fundList = r.data;
        });
    }
    initFund()
  }
}