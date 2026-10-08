import { callApi } from "../api/http.js";
import { copyToClipboard } from './common/clipboardHelper.js';
import { injectToolShellStyles } from './common/uiShell.js';

export default {
  name: 'user-info-query',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
    <div class="tool-shell">
      <el-card shadow="hover" class="tool-shell__card">
        <div class="tool-shell__inner">
          <div class="tool-shell__hero tool-shell__hero--blue">
            <div class="tool-shell__hero-content">
              <div>
                <div class="tool-shell__eyebrow">USER INSPECTOR</div>
                <div class="tool-shell__title">用户信息查询</div>
                <div class="tool-shell__desc">查询用户主信息与嵌套结构数据，保留原有复制与表格展示能力，只调整界面结构与视觉层级。</div>
              </div>
              <div class="tool-shell__stats">
                <div class="tool-shell__stat">
                  <div class="tool-shell__stat-label">当前环境</div>
                  <div class="tool-shell__stat-value">{{ selectedEnv }}</div>
                </div>
                <div class="tool-shell__stat">
                  <div class="tool-shell__stat-label">结果状态</div>
                  <div class="tool-shell__stat-value">{{ userInfoRes ? '已返回' : '待查询' }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="tool-shell__panel tool-shell__panel--soft" style="margin-bottom: 20px;">
            <div class="tool-shell__panel-title">查询条件</div>
            <div class="tool-shell__panel-desc">手机号和 user_no 任填一个；若两个都填写，则以 user_no 为准。</div>
            <el-form label-position="top">
              <el-row :gutter="20">
                <el-col :xs="24" :md="12">
                  <el-form-item label="手机号">
                    <el-input v-model="toBeEncryptedMobile" placeholder="手机号" />
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :md="12">
                  <el-form-item label="User_no">
                    <el-input v-model="user_no" placeholder="助贷user_no" />
                  </el-form-item>
                </el-col>
              </el-row>
              <div class="tool-shell__tip">手机号和 user_no 填任意一个，填写两个时，返回数据以 user_no 为准。</div>
              <div class="tool-shell__actions">
                <el-button type="primary" class="tool-shell__primary-btn" @click="queryUserInfo">查询</el-button>
              </div>
            </el-form>
          </div>

          <div v-if="userInfoRes" class="tool-shell__stack">
            <div v-if="mainTableHeaders.length" class="tool-shell__result">
              <div class="tool-shell__result-head">
                <div>
                  <div class="tool-shell__result-title">主要信息</div>
                  <div class="tool-shell__result-desc">主表字段以平铺方式展示，支持一键复制。</div>
                </div>
                <div class="tool-shell__result-tag">Main Fields</div>
              </div>
              <div class="tool-shell__result-body">
                <el-table :data="mainTableData" border style="width: 100%">
                  <el-table-column
                      v-for="(header, index) in mainTableHeaders"
                      :key="index"
                      :label="header"
                      :prop="header"
                  >
                    <template #default="{ row }">
                      <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                        <span>{{ row[header] }}</span>
                        <el-button type="text" @click="copyToClipboard(row[header])">复制</el-button>
                      </div>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </div>

            <div v-for="(nestedDataArray, nestedKey) in nestedTables" :key="nestedKey" class="tool-shell__result tool-shell__result--teal">
              <div class="tool-shell__result-head">
                <div>
                  <div class="tool-shell__result-title">{{ nestedKey }}</div>
                  <div class="tool-shell__result-desc">嵌套对象结构保留表格展示与复制功能。</div>
                </div>
                <div class="tool-shell__result-tag">Nested Data</div>
              </div>
              <div class="tool-shell__result-body">
                <el-table :data="nestedDataArray" border style="width: 100%">
                  <el-table-column
                      v-for="(value, key) in nestedDataArray[0]"
                      :key="key"
                      :label="key"
                      :prop="key"
                  >
                    <template #default="{ row }">
                      <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
                        <span>{{ row[key] }}</span>
                        <el-button type="text" @click="copyToClipboard(row[key])">复制</el-button>
                      </div>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  `,
  data() {
    return {
      toBeEncryptedMobile: "",
      userInfoRes: "",
      user_no: "",
    };
  },
  computed: {
    parsedUserInfo() {
      try {
        return JSON.parse(this.userInfoRes) || {};
      } catch (error) {
        return {};
      }
    },
    mainTableHeaders() {
      return Object.keys(this.parsedUserInfo).filter(
        (key) => typeof this.parsedUserInfo[key] !== 'object' || this.parsedUserInfo[key] === null
      );
    },
    mainTableData() {
      const dataObject = {};
      this.mainTableHeaders.forEach((key) => {
        dataObject[key] = this.parsedUserInfo[key];
      });
      return [dataObject];
    },
    nestedTables() {
      const nestedData = {};
      Object.keys(this.parsedUserInfo).forEach((key) => {
        const value = this.parsedUserInfo[key];
        if (typeof value === 'object' && value !== null) {
          nestedData[key] = [value];
          console.log('nestedData', nestedData);
        }
      });
      return nestedData;
    },
  },
  methods: {
    async queryUserInfo() {
      this.userInfoRes = `====查询手机号：${this.toBeEncryptedMobile}，勿重复点击====`;
      const params = {
        env: this.selectedEnv,
        mobile: this.toBeEncryptedMobile,
        user_no: this.user_no
      };
      try {
        const response = await callApi('api/query_user', params);
        this.userInfoRes = JSON.stringify(response, null, 2);
      } catch (error) {
        console.error('查询失败', error);
        this.userInfoRes = '查询失败，请重试';
      }
    },
    copyToClipboard(value) {
      copyToClipboard(value, this.$message);
    },
  },
  mounted() {
    injectToolShellStyles();
  }
}
