import { copyToClipboard } from './common/clipboardHelper.js';

export default {
  name: 'random-user-data',
  template: `
    <div>
      <el-button 
        type="primary" 
        @click="getRandomUserInfoBtn"
        style="margin-bottom: 20px;">刷新
      </el-button>
      <el-table :data="tableData" border >
        <el-table-column
          fixed="left"
          label="序号"
          width="60">
          <template #default="scope">
            <span>{{ scope.$index + 1 }}</span>
          </template>
        </el-table-column>
        
        <!-- 动态表头，列宽根据内容自适应 -->
        <el-table-column
          v-for="(key, index) in tableColumns"
          :key="index"
          :label="key"
          :prop="key"
          :min-width="computeColumnWidth(key)"
          :header-cell-style="{ padding: '10px 0', lineHeight: '20px' }"
          :show-overflow-tooltip="false">
          <template #default="scope">
            <div style="display: flex; align-items: center; white-space: nowrap;">
              <span>{{ scope.row[key] }}</span>
              <el-button 
                type="text" 
                icon="el-icon-document-copy" 
                @click="copyToClipboard(scope.row[key])"
                size="small"
                style="margin-left: 8px;">
                复制
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  `,
  data() {
    return {
      rawData: []
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
    computeColumnWidth(key) {
      // 根据字段内容自适应宽度，可视需求调整最小和最大宽度
      let longest = Math.max(...this.rawData.map(row => String(row[key]).length));
      // 计算内容和按钮宽度的总和
      const buttonWidth = 60;  // 按钮宽度（可以根据实际按钮宽度调整）
      return `${Math.max(longest * 10 + buttonWidth, 100)}px`; // 10为字符宽度倍数，可调整
    },
    copyToClipboard(value) {
      copyToClipboard(value, this.$message);
    },
    getRandomUserInfoBtn() {
      fetch('/api/get_random_user_info')
        .then(response => {
          if (!response.ok) {
            throw new Error('网络响应错误');
          }
          return response.json();
        })
        .then(data => {
          if (Array.isArray(data)) {
            this.rawData = data;
          } else {
            this.$message.error("数据格式错误");
          }
        })
        .catch(error => {
          console.error("Error fetching data:", error);
          this.$message.error("网络错误，请稍后再试");
        });
    }
  },
  mounted() {
    this.getRandomUserInfoBtn();
  }
}
