import { callApi } from "../api/http.js";
export default {
  name: 'user-delete',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
  <div>
    <el-form label-width="120px">
      <!-- 手机号输入框 -->
      <el-form-item label="手机号(根据身份证号删除所有信息)：">
        <el-input 
          class="input_box" 
          type="text" 
          v-model="delMobile" 
          placeholder="用户手机号明文"
        />
      </el-form-item>

      <!-- 提交按钮 -->
      <el-form-item>
        <el-button 
          class="submit-button" 
          id="clearBtn" 
          @click="clear" 
          type="primary"
        >
          提交清除
        </el-button>
      </el-form-item>

      <!-- 选择需清除的信息 -->
      <el-form-item label="选择需清除的信息：">
        <el-checkbox-group v-model="selectedDelItems">
          <el-checkbox 
            v-for="item in delItems" 
            :key="item.value" 
            :label="item.value"
            :title="item.title"
            size="large" border 
          >
            {{ item.label }}
          </el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <!-- 清除用户信息结果 -->
      <el-form-item label="清除用户信息结果：">
        <el-input
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 40 }"
          placeholder="清除用户信息结果"
          v-model="delUserInfoRes"
        />
      </el-form-item>
    </el-form>
  </div>
  `,
  data() {
    return {
      // 删除用户相关变量
      delMobile: '',
      delItems: [
          { value: 'del_user', label: '删除用户信息', title: '选择此项会清除所有用户相关信息，包括授信、借还款、绑卡信息' },
          { value: 'del_ocr', label: '删除实名信息', title: '删除实名信息，其他项不删除' },
          { value: 'del_contact', label: '删除联系人信息', title: '删除联系人信息，不会删除其他数据' },
          { value: 'del_detail', label: '删除详细资料信息', title: '删除详细资料信息，不会删除其他数据' },
          { value: 'del_credit', label: '删除授信信息', title: '删除授信信息，不会删除其他数据' },
          { value: 'del_loan', label: '删除借据信息', title: '删除借据信息, 不会删除其他数据' },
          { value: 'del_bind', label: '删除绑卡人信息', title: '删除绑卡信息，不会删除其他数据' },
          { value: 'del_auth', label: '删除权限人信息', title: '删除权限人相关信息，不会删除其他数据' },
          { value: 'del_repay', label: '删除还款信息', title: '删除还款信息，不会删除其他数据' },
      ],
      selectedDelItems: [],
      delUserInfoRes: '',
    };
  },
  computed: {
  },
  methods: {
    async clear() {
      this.delUserInfoRes = "====清除信息手机号：{}，勿重复点击====".replace("{}", this.delMobile);
      const data = {
        env: this.selectedEnv,
        mobile: this.delMobile,
        items: this.selectedDelItems,
      };
      console.log("clear:data", data);

      const response = await callApi('api/del_user', data);
      console.log("clear:response", response, response.ok);
      this.delUserInfoRes = JSON.stringify(response, null, 2);
    },
  },
}