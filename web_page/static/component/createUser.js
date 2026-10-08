import { callApi } from '../api/http.js'
export default {
  name: 'app-user-create',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `  <div>
    <el-form :model="createUserData" label-width="120px">
      <el-row :gutter="20">
        
        <!-- 用户状态 -->
        <el-col :span="9">
          <el-form-item label="用户状态：">
            <el-select 
              v-model="createUserData.selectedCreateUserNode" 
              placeholder="请选择用户状态"
              style="width: 100%;" 
              clearable
            >
              <el-option 
                v-for="option in userStatusOptions" 
                :key="option.value" 
                :label="option.label" 
                :value="option.value"
              />
            </el-select>
          </el-form-item>
        </el-col>
        
        <!-- 渠道选择 -->
        <el-col :span="5">
          <el-form-item label="选择渠道：">
            <el-select 
              v-model="createUserData.selectedCreateUserChannel" 
              placeholder="请选择渠道"
              style="width: 100%;" 
              clearable
            >
              <el-option 
                v-for="option in channelOptions" 
                :key="option.value" 
                :label="option.label" 
                :value="option.value"
              />
            </el-select>
          </el-form-item>
        </el-col>

        <!-- 产品选择 -->
        <el-col :span="5">
          <el-form-item label="选择产品：">
            <el-select 
              v-model="createUserData.selectedCreateUserProduct" 
              placeholder="请选择产品"
              style="width: 100%;" 
              clearable
            >
              <el-option 
                v-for="option in productOptions" 
                :key="option.value" 
                :label="option.label" 
                :value="option.value"
              />
            </el-select>
          </el-form-item>
        </el-col>


        <!-- 账号个数 -->
        <el-col :span="5">
          <el-form-item label="账号个数：">
            <el-input 
              v-model="createUserData.countNums" 
              type="number" 
              placeholder="默认为1"
              style="width: 100%;" 
              clearable
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <!-- 指定机构 -->
        <el-col :span="9">
          <el-form-item label="指定机构：">
            <el-select 
              v-model="createUserData.selectedFundCodes" 
              multiple 
              filterable 
              clearable 
              placeholder="为空走分发，指定机构则走tds-mock" 
              class="custom-select"
              style="width: 100%;"
            >
              <el-option 
                v-for="item in createUserData.fund_code" 
                :key="item.fund_code" 
                :label="item.fund_name_code" 
                :value="item.fund_code"
              />
            </el-select>
          </el-form-item>
        </el-col>
        
        <!-- 指定手机号 -->
        <el-col :span="5">
          <el-form-item label="指定手机号：">
            <el-input 
              v-model="createUserData.createUserMobile" 
              type="number" 
              placeholder="空则随机"
              style="width: 100%;" 
              clearable
            />
          </el-form-item>
        </el-col>

        <!-- 指定身份证号 -->
        <el-col :span="5">
          <el-form-item label="指定身份证号：">
            <el-input 
              v-model="createUserData.createUserIdNo" 
              type="text" 
              placeholder="空则随机"
              style="width: 100%;" 
              clearable
            />
          </el-form-item>
        </el-col>

        <!-- 指定姓名 -->
        <el-col :span="5">
          <el-form-item label="指定姓名：">
            <el-input 
              v-model="createUserData.createUserName" 
              type="text" 
              placeholder="空则随机"
              style="width: 100%;" 
              clearable
            />
          </el-form-item>
        </el-col>
        
      </el-row>

      <el-row :gutter="20">
        <!-- 提交按钮 -->
        <el-col :span="24">
          <el-form-item>
            <el-button 
              class="submit-button" 
              id="submitCreditBtn" 
              @click="createUser" 
              type="primary"
            >
              创建
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <!-- 查询结果 -->
        <el-col :span="24">
          <el-form-item label="查询结果：">
            <el-input
              type="textarea"
              :autosize="{ minRows: 2, maxRows: 40 }"
              placeholder="创建用户结果"
              v-model="createUserData.createUserRes"
              style="width: 100%;"
            />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </div>
  `,
  data() {
    return {
      createUserData: {
        createUserMobile: "",
        createUserIdNo: "",
        createUserName: "",
        createUserRes: "",
        fund_code: [], // 从后端动态获取
        selectedCreateUserNode: 'user_logged',
        selectedCreateUserChannel: 'LXJ_APP',
        selectedCreateUserProduct: 'PILOT_APP',
        selectedFundCodes: [],
        countNums: 1,
      },
      channelOptions: [
        { value: "LXJ_APP", label: "乐享借APP: LXJ_APP" },
        { value: "BY_APP", label: "贝赢APP: BY_APP" },
        { value: "HUB_TEST", label: "H5: HUB_TEST" },
      ],
      productOptions: [
        { value: "PILOT_APP", label: "PILOT_APP" },
        { value: "PILOT_HUB", label: "PILOT_HUB" },
      ],
      userStatusOptions: [
        { value: "user_logged", label: "登录并刷新首页" },
        { value: "identity", label: "已提交身份证，进入人脸识别节点" },
        { value: "face", label: "已提交人脸，进入联系人节点" },
        { value: "contact", label: "联系人填写完成，未提交" },
        { value: "profile", label: "详细资料填写完成，未提交" },
        { value: "bind", label: "已选择机构，进入绑卡节点" },
        { value: "submitted", label: "授信提交完成" },
      ],
    };
  },
  computed: {
  },
  methods: {
    // 实现调用创建用户接口
    async createUser() {
      this.createUserData.createUserRes = "====执行至节点：{}，勿重复点击====".replace("{}", this.createUserData.selectedCreateUserNode);
      console.log("createUser::data", this.selectedEnv, );
      const data = {
        nums: this.createUserData.countNums,
        env: this.selectedEnv,
        channel: this.createUserData.selectedCreateUserChannel,
        product_code: this.createUserData.selectedCreateUserProduct,
        assign_node: this.createUserData.selectedCreateUserNode,
        mobile_no: this.createUserData.createUserMobile,
        id_no: this.createUserData.createUserIdNo,
        name: this.createUserData.createUserName,
        fund_code: this.createUserData.selectedFundCodes
      };
      console.log("Data", data)
      try {
        const response = await callApi("api/create_users", data);
        if (response.success === 0) {
          const responseData = response.res;
          console.log("createUser::responseData", responseData)
          this.createUserData.createUserRes = JSON.stringify(responseData, null, 2);
          } else {
            new Error("Network response was not ok.");
          }
      } catch (error) {
        console.error(error);
        // 处理错误，例如显示错误提示信息
      } finally {
      }
    },
    async getFundData() {
      const env = this.selectedEnv;
      console.log("env", env);
      // const fundUrl = `api/fund-code-list?env=${encodeURIComponent(env)}`;
      const fundUrl = `api/fund-code-list?env=${encodeURIComponent(env)}`;
      try {
        const data = await callApi(fundUrl, {}, 'GET'); // 发起 GET 请求
        console.log("fund_code---1",data.data); // 处理返回的数据
        this.createUserData.fund_code = data.data
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
  },
  mounted() {
    if (this.selectedEnv) {
      this.getFundData();  // 直接调用
    } else {
      console.warn("selectedEnv 未初始化，将延迟调用 getFundData");
      const interval = setInterval(() => {
        if (this.selectedEnv) {
          this.getFundData();
          clearInterval(interval);
        }
      }, 100);  // 每 100ms 检查一次
    }
  }
}
