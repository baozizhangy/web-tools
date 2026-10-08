import { callApi } from "../api/http.js";
export default {
  name: 'hub-full-flow',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
  <div>
    <div>
      <label for="ChannelIdSelect">选择对应的渠道：</label>
      <el-select id="ChannelIdSelect" v-model="channelId">
        <el-option v-for="option in channelIdOptions" :key="option.value" :label="option.label"
          :value="option.value"></el-option>
      </el-select>
      <el-button @click="getLandChannelUrl" class="query-button"><i class="fas fa-search"></i>查询</el-button>
    </div>
    <div>
      <label>生成结果:</label>
      <textarea class="output-box" ref="getLandChannelUrlsTextarea" v-model="getLandChannelDataRes"
        placeholder="生成结果" @input="adjustTextareaHeight('getLandChannelUrlsTextarea')"></textarea>
    </div>
  </div>
  `,
  data() {
    return {
      getLandChannelDataRes: "",
      channelId: "",
      channelIdOptions: [
          { value: 'HUB_XIMALAYA', label: '喜马拉雅' },
          { value: 'HUB_MOGUJIE', label: '蘑菇街' },
          { value: 'HUB_SINA', label: '新浪' },
          { value: 'HUB_YUNBAOBAO', label: '云宝宝' },
          { value: 'HUB_XIAOYING', label: '小赢卡贷' }
      ],
    };
  },
  computed: {
  },
  methods: {
    async getLandChannelUrl() {
      const data = {
        env: this.selectedEnv,
        channelId: this.channelId,
      }
      try {
          this.getLandChannelDataRes = null;
          this.errorMessage = null;
          if (!data.env || !data.channelId) {
              new Error("缺少必填参数:请确保已选择环境、选择渠道");
          }
          const response = await fetch("api/get_land_channel_url", {
              method: 'POST',
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify(data)
          });
          if (!response.ok) {
              new Error(`Response failed: ${response.status} ${response.statusText}`);
          }

          const responseData = await response.json();
          this.getLandChannelDataRes = JSON.stringify(responseData, null, 2);

      } catch (error) {
          console.error("Error querying codes", error.message);
          this.errorMessage = error.message || "查询过程中出现错误，请稍后重试";
          this.getLandChannelDataRes = this.errorMessage;
      }
    },
  },
}