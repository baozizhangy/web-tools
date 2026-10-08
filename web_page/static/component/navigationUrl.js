import { injectToolShellStyles } from './common/uiShell.js';

export default {
  name: 'navigation-url',
  template: `
    <div class="tool-shell">
      <el-card shadow="hover" class="tool-shell__card">
        <div class="tool-shell__inner">
          <div class="tool-shell__hero tool-shell__hero--violet">
            <div class="tool-shell__hero-content">
              <div>
                <div class="tool-shell__eyebrow">NAVIGATION HUB</div>
                <div class="tool-shell__title">书签导航</div>
                <div class="tool-shell__desc">集中管理常用链接，保留原有新增与跳转功能，只做卡片布局和信息层级优化。</div>
              </div>
              <div class="tool-shell__stats">
                <div class="tool-shell__stat">
                  <div class="tool-shell__stat-label">分类数量</div>
                  <div class="tool-shell__stat-value">{{ Object.keys(groupedData).length }}</div>
                </div>
                <div class="tool-shell__stat">
                  <div class="tool-shell__stat-label">链接总数</div>
                  <div class="tool-shell__stat-value">{{ rawData.length }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="tool-shell__panel tool-shell__panel--soft">
            <div class="tool-shell__panel-title">分类浏览</div>
            <div class="tool-shell__panel-desc">按分类查看常用地址，每组保留新增入口。</div>
            <el-row :gutter="20">
              <template v-for="(rowTypes, rowIndex) in groupedRows" :key="'row-' + rowIndex">
                <el-col :span="24" v-if="rowIndex > 0">
                  <el-divider></el-divider>
                </el-col>
                <el-col
                  v-for="type in rowTypes"
                  :key="'type-' + type"
                  :xs="24"
                  :sm="12"
                  :md="6"
                  style="margin-bottom: 20px;"
                >
                  <div class="tool-shell__choice-card" style="height: 100%; background: linear-gradient(180deg, #ffffff 0%, #fbfcff 100%);">
                    <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 12px;">
                      <div class="tool-shell__choice-title">{{ type }}</div>
                      <el-button type="primary" size="small" @click="openAddDialog(type)">新增</el-button>
                    </div>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                      <el-link
                        v-for="item in groupedData[type]"
                        :key="'link-' + item.title"
                        :href="item.url"
                        target="_blank"
                        :underline="false"
                        :title="item.remark"
                        style="padding: 6px 12px; background: #f5f7fb; border: 1px solid #e6ecf5; border-radius: 999px;"
                      >
                        {{ item.title }}
                      </el-link>
                    </div>
                  </div>
                </el-col>
              </template>
            </el-row>
          </div>
        </div>
      </el-card>

      <el-dialog title="新增链接" v-model="dialogVisible">
        <el-form :model="form" label-position="top">
          <el-form-item label="Type" :rules="[{ required: true, message: '请输入分类类型', trigger: 'blur' }]">
            <el-input v-model="form.type"></el-input>
          </el-form-item>
          <el-form-item label="Title" :rules="[{ required: true, message: '请输入标题', trigger: 'blur' }]">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
          <el-form-item label="URL" :rules="[{ required: true, message: '请输入URL', trigger: 'blur' }]">
            <el-input v-model="form.url"></el-input>
          </el-form-item>
          <el-form-item label="Remark">
            <el-input v-model="form.remark"></el-input>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAdd">提交</el-button>
        </template>
      </el-dialog>
    </div>
  `,
  data () {
    return {
      rawData: [],
      dialogVisible: false,
      form: {
        type: '',
        title: '',
        url: '',
        remark: ''
      }
    };
  },
  computed: {
    groupedData () {
      return this.rawData.reduce((acc, item) => {
        (acc[item.type] = acc[item.type] || []).push(item);
        return acc;
      }, {});
    },
    groupedRows () {
      const types = Object.keys(this.groupedData);
      const rows = [];
      for (let i = 0; i < types.length; i += 4) {
        rows.push(types.slice(i, i + 4));
      }
      return rows;
    }
  },
  methods: {
    fetchData () {
      fetch('/api/nav/get')
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          this.rawData = data;
        }
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    openAddDialog (type) {
      this.form = {
        type,
        title: '',
        url: '',
        remark: ''
      };
      this.dialogVisible = true;
    },
    submitAdd () {
      if (!this.form.type || !this.form.title || !this.form.url) {
        this.$message.error('请填写必填字段');
        return;
      }
      fetch('/api/nav/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.form)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('新增失败');
        }
        return response.json();
      })
      .then(() => {
        this.$message.success('新增成功');
        this.dialogVisible = false;
        this.fetchData();
      })
      .catch(error => {
        console.error('Error adding navigation:', error);
        this.$message.error('新增失败，请稍后再试');
      });
    }
  },
  mounted () {
    injectToolShellStyles();
    this.fetchData();
  }
};
