
export default {
  name: 'credit-node',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
    <div>
      <div>
        <label>手机号:
          <el-input v-model="mobile" type="text" placeholder="请输入手机号" clearable
            style="width: 240px"/>
        </label>
        <label for="eventCodeSelect">选择要修改授信节点：</label>
        <el-select id="eventCodeSelect" v-model="pilotCodes" style="width: 360px">
          <el-option v-for="option in pilotCodeOptions" :key="option.value" :label="option.label"
          :value="option.value"></el-option>
        </el-select><br>
        <el-button @click="updateScencePilots" type="primary">修改</el-button>
      </div>
      <div>
        <el-input 
          type="textarea" 
          autosize 
          placeholder="更改结果" 
          v-model="updateScencePilotDataRes"
        />
      </div>
    </div>
  `,
  data() {
    return {
      updateScencePilotDataRes: "",
      pilotCodes: "",
      mobile: "",
      pilotCodeOptions: [
        { value: 'pilotIdentityV2', label: '身份证页' },
        { value: 'pilotFaceV2', label: '活体页' },
        { value: 'pilotContactV2', label: '联系人页' },
        { value: 'pilotDetailsV2', label: '详细资料页' }
      ],
    };
  },
  computed: {
    tableColumns() {
      const columns = this.rawData.length > 0 ? Object.keys(this.rawData[0]) : [];
      return columns;
    },
    tableData() {
      return this.rawData;
    }
  },
  methods: {
    async updateScencePilots() {
      const data = {
          env: this.selectedEnv,
          mobile: this.mobile,
          pilotcode: this.pilotCodes
      }
      try {
        this.updateScencePilotDataRes = null;
        this.errorMessage = null;
        if (!data.env || !data.mobile || !data.pilotcode) {
          new Error("缺少必填参数:请确保已选择环境、输入手机号、选择对应节点");
        }
        const response = await fetch("api/update_scene_pilots", {
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
        this.updateScencePilotDataRes = JSON.stringify(responseData, null, 2);

      } catch (error) {
        console.error("Error querying codes", error.message);
        this.errorMessage = error.message || "更新过程中出现错误，请稍后重试";
        this.updateScencePilotDataRes = this.errorMessage;
      }
    },
  },
  mounted() {
  }
}