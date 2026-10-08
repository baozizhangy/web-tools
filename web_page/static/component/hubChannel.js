import {callApi} from '../api/http.js'

export default {
  name: 'hub-user-create',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
  <div>
    <el-form :model="channelPersonnelData" label-width="120px">
      <el-row :gutter="20">
        <el-col :span="8" v-for="(field, key) in inputFields" :key="key">
          <el-form-item :label="field.label">
            <el-input 
              v-model="channelPersonnelData[key]" 
              :placeholder="field.placeholder" 
              clearable
              class="el-input-box"
              type="text"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <!-- HUB 输入部分 -->
        <el-col :span="8" v-for="(field, key) in hubFields" :key="key">
          <el-form-item :label="field.label">
            <el-input 
              v-model="channelPersonnelData[key]" 
              :placeholder="field.placeholder" 
              clearable
              class="el-input-box"
              type="text"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item>
        <el-button type="primary" @click="getFakerUserInfo('all')">
          <el-icon><Refresh /></el-icon>
          随机
        </el-button>
        <el-button type="primary" @click="resetFakerUserInfo">
          <el-icon><Delete /></el-icon>
          重置
        </el-button>
      </el-form-item>

      <!-- 选择 HUB 渠道 -->
      <el-form-item label="选择HUB渠道：">
        <el-select v-model="selectedChannel" @change="queryChannel" clearable style="width: 288px">
          <el-option 
            v-for="option in hubChannelOptions" 
            :key="option.value" 
            :label="option.label" 
            :value="option.value"
          />
        </el-select>
      </el-form-item>

      <!-- 请求按钮 -->
      <el-form-item>
        <el-button 
          plain
          v-for="method_info in channelBtnData" 
          :key="method_info.method" 
          v-html="method_info.method_name" 
          :data-method_type="method_info.method_type" 
          @click="channelMethodButton(method_info.method, 'get_param')"
        />
      </el-form-item>
      <el-button type="primary" @click="pushChannelRequest">
        <el-icon class="el-icon"><Upload /></el-icon>
        提交请求
      </el-button>

      <!-- 渠道请求内容 -->
      <el-form-item>
        <el-input 
          type="textarea" 
          autosize 
          placeholder="渠道请求内容" 
          v-model="jsonChannelEditorData"
        />
<!--        <json-pretty-->
<!--          :jsonData="jsonChannelEditorData" -->
<!--          :deep="5"-->
<!--        />-->
      </el-form-item>
    </el-form>
  </div>
  `,
  data() {
    return {
      channelPersonnelData: {
        channelMobile: null,
        channelIdNo: null,
        channelCustName: null,
        channelBankCardNo: null,
        channelUserNo: null,
        channelCheckNo: null,
        channelCreditNo: null,
        channelDrawNo: null,
        channelRepayNo: null,
        hubUserId: null,
        hubOrderNo: null,
        hubSubOrderNo: null,
        hubBindCardSerialNo: null,
        hubDrawSerialNo: null,
        hubBindRelationId: null,
      },
      inputFields: {
        channelMobile: {
          label: '手机号',
          placeholder: '点击随机按钮生成'
        },
        channelIdNo: {
          label: '身份证',
          placeholder: '点击随机按钮生成'
        },
        channelCustName: {
          label: '姓名',
          placeholder: '点击随机按钮生成'
        },
        channelBankCardNo: {
          label: '银行卡',
          placeholder: '点击随机按钮生成'
        },
        channelUserNo: {
          label: '渠道用户号',
          placeholder: '点击随机按钮生成'
        },
        channelCheckNo: {
          label: '渠道准入流水号',
          placeholder: '点击随机按钮生成'
        },
        channelCreditNo: {
          label: '渠道授信流水号',
          placeholder: '点击随机按钮生成'
        },
        channelDrawNo: {
          label: '渠道借款流水号',
          placeholder: '点击随机按钮生成'
        },
        channelRepayNo: {
          label: '渠道还款流水号',
          placeholder: '点击随机按钮生成'
        },
      },
      hubFields: {
        hubUserId: {
          label: 'HUB userId',
          placeholder: '手输，关联：民生|易借速贷V2'
        },
        hubOrderNo: {
          label: 'HUB母订单号',
          placeholder: '部分接口使用，手输'
        },
        hubSubOrderNo: {
          label: 'HUB子订单号',
          placeholder: '部分接口使用，手输'
        },
        hubBindCardSerialNo: {
          label: 'HUB绑卡流水号',
          placeholder: '部分接口使用，手输'
        },
        hubBindRelationId: {
          label: 'bind_relation_id',
          placeholder: '部分渠道使用，手输'
        },
        hubDrawSerialNo: {
          label: 'HUB借款流水号',
          placeholder: '部分接口使用，手输'
        },
      },
      hubChannelOptions: [
        { value: 'HUB_HUOLALA', label: 'HUB_HUOLALA 货拉拉' },
        { value: 'HUB_ZHONGMI', label: 'HUB_ZHONGMI 众米' },
        { value: 'HUB_XIAOHUA', label: 'HUB_XIAOHUA 小花钱包' },
        { value: 'HUB_YIJIESUDAI_V2', label: 'HUB_YIJIESUDAI_V2 易借速贷V2' },
        { value: 'HUB_JUZI', label: 'HUB_JUZI 橘子' },
        { value: 'HUB_MINSHENG', label: 'HUB_MINSHENG 民生' },
        { value: 'HUB_YIXIANGHUA', label: 'HUB_YIXIANGHUA 宜享花' },
        { value: 'HUB_TIANMIAN', label: 'HUB_TIANMIAN 天冕' },
        { value: 'HUB_TIANMIAN_V2', label: 'HUB_TIANMIAN_V2 天冕v2' },
        { value: 'HUB_SHIGUANGFENQI', label: 'HUB_SHIGUANGFENQI 时光分期' },
        { value: 'HUB_HAOFENQI', label: 'HUB_HAOFENQI 好分期' },
        { value: 'HUB_HAOFENQI_S1', label: 'HUB_HAOFENQI_S1 好分期S1' },
        { value: 'HUB_58HAOJIE', label: 'HUB_58HAOJIE 58好借' },
        { value: 'HUB_FUYUANHUI', label: 'HUB_FUYUANHUI 富元汇' },
        { value: 'HUB_XIAOYING', label: 'HUB_XIAOYING 小赢' },
        { value: 'HUB_XINYONGFEI', label: 'HUB_XINYONGFEI 信用飞' },
        { value: 'HUB_XIAOXIANG_V2', label: 'HUB_XIAOXIANG_V2 小象V2' },
        { value: 'HUB_FEICHANGZHUN', label: 'HUB_FEICHANGZHUN 非常准' },
        { value: 'HUB_YUNBAOBAO', label: 'HUB_YUNBAOBAO 云宝宝' },
        { value: 'HUB_JIUFU_V2', label: 'HUB_JIUFU_V2 玖富v2' },
        { value: 'HUB_NIWODAI', label: 'HUB_NIWODAI 你我贷' },
        { value: 'HUB_NIWODAI_S1', label: 'HUB_NIWODAI_S1 你我贷s1' },
        { value: 'HUB_NIWODAI_S2', label: 'HUB_NIWODAI_S2 你我贷s2' },
        { value: 'HUB_SHENGBEI', label: 'HUB_SHENGBEI 省呗' },
        { value: 'HUB_TONGCHENG', label: 'HUB_TONGCHENG 同程' },
        { value: 'HUB_GUOMEI', label: 'HUB_GUOMEI 国美' },
        { value: 'HUB_XIECHENG_V2', label: 'HUB_XIECHENG_V2 携程v2' },
        { value: 'HUB_XIECHENG_V3', label: 'HUB_XIECHENG_V3 携程v3' },
        { value: 'HUB_WEIXIN', label: 'HUB_WEIXIN 维信' },
        { value: 'LXJ_APP', label: 'LXJ_APP' },
        { value: 'HUB_TEST', label: 'HUB_TEST' }
      ],
      channelBtnData: {},
      jsonChannelEditorData: null,
      selectedChannel: ''
    };
  },
  computed: {
  },
  methods: {
    resetFakerUserInfo() {
      // 遍历对象的所有属性并将它们设置为 null
      for (const key in this.channelPersonnelData) {
        if (Object.prototype.hasOwnProperty.call(this.channelPersonnelData, key)) {
          this.channelPersonnelData[key] = null;
        }
      }
    },
    async getFakerUserInfo(infoType) {
      // const data = JSON.stringify(result)
      const data = await callApi("api/channel/get_faker_user_info", "")

      this.channelPersonnelData.channelMobile = data.channelMobile;
      this.channelPersonnelData.channelIdNo = data.channelIdNo;
      this.channelPersonnelData.channelCustName = data.channelCustName;
      this.channelPersonnelData.channelBankCardNo = data.channelBankCardNo;
      this.channelPersonnelData.channelUserNo = data.channelUserNo;
      this.channelPersonnelData.channelCheckNo = data.channelCheckNo;
      this.channelPersonnelData.channelCreditNo = data.channelCreditNo;
      this.channelPersonnelData.channelDrawNo = data.channelDrawNo;
      this.channelPersonnelData.channelRepayNo = data.channelRepayNo;
    },

    async pushChannelRequest() {
      const params = {
        env:  this.selectedEnv,
        data: this.jsonChannelEditorData
      };
      console.log("Vue.version::", Vue.version); // 查看当前 Vue 的版本号
      // console.log("window.VueJsonPretty", window.VueJsonPretty);
      console.log("pushChannelRequest:params", params);
      const response = await callApi("api/channel/push_channel_handle", params);
      let htmlMessage = `<textarea rows="3" style="width: 100%;">${JSON.stringify(response)}</textarea>`;
      const res = JSON.stringify(response);

      this.$notify({
        title: '调用hub-service返回',
        customClass: 'channel-notify',
        dangerouslyUseHTMLString: true,
        duration: 0,
        message: res
      });
    },
    // 实现选择渠道查询渠道方法
    async queryChannel(channel) {
      this.channelBtnData = {};
      this.selectedChannel = channel;
      if (channel !== '0') {
        const params = {
          env: this.selectedEnv,
          channel: channel,
          method: "get_channel_methods",
          data: this.jsonChannelEditorData
        };
        const response = await callApi("api/channel/request_channel_methods", params);
        console.log("queryChannel:response", response);
        this.channelBtnData = await response["data"];
        console.log("queryChannel:this.channelBtnData", this.channelBtnData);
      }
    },
    // 实现渠道方法按钮点击事件
    async channelMethodButton(method, method_type) {
      console.log("channelMethodButton:method", method, "method_type", method_type);
      let channelData;
      if (method_type === 'get_param') {
        channelData = this.channelPersonnelData;
      } else if (method_type === 'push_data') {
        channelData = this.jsonChannelEditorData;
      }
      const params = {
        env: this.selectedEnv,
        channel: this.selectedChannel,
        method: method,
        data: channelData
      };
      const result = await callApi("api/channel/request_channel_methods", params);
      if (method_type === 'get_param') {
        this.jsonChannelEditorData = JSON.stringify(result.data, null, 2);
        // this.handleJsonChange()

      } else if (method_type === 'push_data') {
        // 调用后端接口，并获取结果
        // 假设结果存储在变量 response 中
        // 生成一个唯一的 ID
        const id = Date.now();
        console.log("channelMethodButtonClick:result.data.data", result);
        // 将结果添加到结果数组中
        this.channelResults.push({ id, text: result, method_type });
      }

      // 返回一个 Promise 对象，以便在点击后执行其他逻辑
      return Promise.resolve();
    },
  },
  mounted() {
  }
}
