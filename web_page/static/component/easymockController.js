import {callApi} from "../api/http.js";
import {copyToClipboard} from './common/clipboardHelper.js';

export default {
  name: 'mock-data',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
  <div>
    <span>项目：</span>
    <el-select id="mockProject" v-model="mockData.selectedValue.projectID"
      @change="getMockData('project', mockData.selectedValue.projectID)"
      clearable
      style="width: 100px"
      placeholder="请选择项目">
      <el-option v-for="(item, index) in mockData.param.projectList" :key="index" :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>

    <span>组/机构：</span>
    <el-select id="mockGroup" v-model="mockData.selectedValue.groupID" style="width: 200px"
      @change="getMockData('group', mockData.selectedValue.groupID)" clearable filterable
      placeholder="请选择组">
      <el-option v-for="(item, index) in mockData.param.groupList" :key="index" :label="item.group"
          :value="item.group">
      </el-option>
    </el-select>
    <el-button primary title="刷新时拉取easymock新增配置到数据库" style="float: right; padding-left: 20px"
      @click="refreshMock">刷新</el-button>
    <el-link type="success" icon="el-icon-edit"
      href="http://mockjs.com/0.1/editor.html#help">mock.js在线调试</el-link>
    <br><br>

    <el-tabs type="border-card">
      <el-tab-pane label="接口配置">
        <span>接口/方法：</span>
        <el-select id="mockMethod" v-model="mockData.selectedValue.methodID" style="width: 480px;"
          @change="getMockData('method', mockData.selectedValue.methodID)" clearable filterable
          placeholder="请选择接口">
          <el-option v-for="(item, index) in mockData.param.methodList" :key="index"
            :label="item.method" :value="item.method_id" :title="item.description">
            <span style="float: left">{{ item.method }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px"> {{ item.description }}
            </span>
          </el-option>
        </el-select>

        <el-button type="primary" title="查询easymock当前生效的mock信息"
            @click="getMockData('easymock', mockData.selectedValue.methodUrl)">
          <el-icon><Search /></el-icon>
          查询当前easymock配置
        </el-button><br><br>
        <span>该接口mock模板（ID: 描述）：</span>
        <el-select id="mockDataTemp" v-model="mockData.selectedValue.mockTempID"
          @change="updateMockDataInput(mockData.selectedValue.mockTempID)" clearable filterable
          style="width: 240px"
          placeholder="请选择模板">
          <!--                   allow-create default-first-option-->
          <el-option v-for="(item, index) in mockData.param.mockTempList" :key="index"
            :label="item.data_id+':'+item.description" :value="item.data_id"
            :title="item.description">
          </el-option>
        </el-select>

        <el-button type="primary" icon="el-icon-edit" title="新增mock模板"
          @click="createMockData">保存模板</el-button>
        <el-tooltip content="配置选择的模板到easymock，以ID对应的模板为准，不取下方展示，应先保存为模板后配置" placement="top"
          effect="light">
          <el-button type="primary" title="配置选择的模板到easymock" @click="pushMockData()">按模板配置<i
            class="el-icon-upload el-icon--right"></i></el-button>
        </el-tooltip>
        <br><br>
        <el-row :gutter="20">
          <el-col :span="11">
            <div>mock数据/模板：新增模板时使用以下内容关联method_id
              <el-input type="textarea" autosize placeholder="mock模板内容"
                v-model="mockTempData">
              </el-input>
            </div>
          </el-col>
          <el-col :span="13">
            <div>备注信息暂不支持修改删除，根据id到easymock_method_remark修改
              <el-input type="textarea" autosize placeholder="备注内容"
                v-model="mockData.methodRemarkData">
              </el-input>
              <el-button plain @click="creditRemark()">增加备注信息</el-button>
              <br><br>
              <el-descriptions title="备注信息：" :column="1">
                <el-descriptions-item
                  v-for="(item, index) in mockData.selectedValue.methodRemarkList"
                  :key="index" :label="'remark_id:'+item.remark_id+'：'+item.title">
                  {{ item.remark_data }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="场景配置" @click="getMockData('scene', mockData.selectedValue.groupID)">
        <el-button type="primary" icon="el-icon-search"
            @click="getMockData('scene', mockData.selectedValue.groupID)">查询场景配置</el-button>
        <el-button type="primary" icon="el-icon-edit" @click="editMockScene()">新增场景配置</el-button>
        <br><br>

        <el-table :data="mockData.param.mockSceneList" border stripe :fit="true"
          style="width: 100%">
          <el-table-column prop="scene_id" width="100" label="场景编号"></el-table-column>
          <el-table-column prop="title" width="120" label="标题"></el-table-column>
          <el-table-column prop="group" width="120" label="机构"></el-table-column>
          <el-table-column prop="data_id_list" label="模板列表"></el-table-column>
          <el-table-column prop="description" label="描述"></el-table-column>
          <el-table-column width="160" label="操作" v-slot="scope">
            <el-button @click="executeMockScene(scope.row)" plain type="primary"
              size="small">应用</el-button>
            <el-button @click="editMockScene(scope.row)" plain type="primary"
              size="small">编辑</el-button>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!--  场景配置更新  -->
    <el-dialog title="场景配置" :visible.sync="dialogMockScene"">
      <el-form :model="mockData.updateForm">
        <el-form-item label="场景标题" :label-width="mockData.param.formLabelWidth">
          <el-input v-model="mockData.updateForm.title" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="模板ID列表" :label-width="mockData.param.formLabelWidth">
          <el-input v-model="mockData.updateForm.data_id_list" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="详细描述" :label-width="mockData.param.formLabelWidth">
          <el-input v-model="mockData.updateForm.description" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
          <el-button @click="changIsShow('dialogMockScene')">取 消</el-button>
          <el-button type="primary" @click="changeMockScene()">确 定</el-button>
      </div>
    </el-dialog>
</div>
  `,
  data() {
    return {
      mockData: {
        param: {
          projectList: [
            {value: "64b50b37cce8c8002247db57", label: "goa"},
            {value: "64eed9a6802f2b00233fa9cb", label: "gos"},
            // { value: "66b18a357e1379001edd0218", label: "dev-bm-goa"},
            {value: "66d195187e1379001edd0272", label: "sit-bm-goa"}
          ],
          groupList: [],
          methodList: [],
          mockTempList: [],
          methodRemarkData: "",
          formLabelWidth: '120px',
          mockSceneList: []
        },
        updateForm: {
          scene_id: '',
          title: '',
          group: '',
          dataIdList: '',
          description: ''
        },
        selectedValue: {
          projectID: "",
          groupID: "",
          methodID: "",
          methodUrl: "",
          mockTempID: "",
          methodRemarkList: []
        }
      },
      dialogMockScene: false,
      mockTempData: "",
    };
  },
  computed: {},
  methods: {
    async getMockData(type, data) {
      if (type === "project") {
        this.mockData.selectedValue.groupID = "";
        this.mockData.selectedValue.methodID = "";
        this.mockData.selectedValue.methodUrl = "";
        this.mockData.selectedValue.mockTempID = "";
        this.mockData.selectedValue.methodRemarkList = [];
        this.mockTempData = ""
      }
      if (type === "group") {
        this.mockData.selectedValue.methodID = "";
        this.mockData.selectedValue.methodUrl = "";
        this.mockData.selectedValue.mockTempID = "";
        this.mockData.selectedValue.methodRemarkList = [];
        this.mockTempData = ""
      }
      if (type === "method") {
        this.mockData.selectedValue.methodUrl = "";
        this.mockData.selectedValue.mockTempID = "";
        this.mockTempData = ""
        const selectedMethodData = this.mockData.param.methodList.find(temp => temp.method_id === data);
        this.mockData.selectedValue.methodUrl = selectedMethodData.url || '';
      }
      if (type === "easymock") {
        data = {
          "projectID": this.mockData.selectedValue.projectID,
          "methodURL": this.mockData.selectedValue.methodUrl
        }
      }
      if (type === "scene") {
        data = {
          "groupID": this.mockData.selectedValue.groupID,
        }
      }
      const params = {
        env: this.selectedEnv,
        optionType: type,
        data: data
      };
      const response = await callApi("api/mock/get_mock_data", params)
      if (response.code === "0") {
        if (response.res_type === "group") {
          this.mockData.param.groupList = response.data;
        } else if (response.res_type === "method") {
          this.mockData.param.methodList = response.data;
        } else if (response.res_type === "mock_temp_data") {
          this.mockData.param.mockTempList = response.data;
          this.mockData.selectedValue.methodRemarkList = response.remark;
        } else if (response.res_type === "easymock_data") {
          try {
            this.mockTempData = JSON.stringify(JSON.parse(response.data), null, 2);
          } catch (error) {
            console.error("该模板数据非Json格式，可能存在注释，按非Json处理：", error);
            this.mockTempData = response.data;
          }
        } else if (response.res_type === "scene_list") {
          if (response.data.length === 0) {
            this.mockData.selectedValue.mockSceneID = "";
          } else {
            this.mockData.param.mockSceneList = response.data;
          }
        }
      }
    },
    async pushMockData() {
      try {
        const data = {
          mockTempID: this.mockData.selectedValue.mockTempID,
        };
        const response = await callApi("api/mock/push_mock_data", data);

        if (response && response.message) {
          this.message = response.message;
          this.$message({
            type: 'success',
            message: '提交更新easymock 成功',
          });
        } else {
          console.warn('Invalid response format');
          this.$message({
            type: 'warning',
            message: '响应格式无效',
          });
        }
      } catch (error) {
        console.error('pushMockData error:', error);
        this.$message({
          type: 'error',
          message: '提交更新easymock 失败',
        });
      }
    },
    async createMockData() {
      try {
        const {value} = await this.$prompt('请简洁的为该模板添加描述', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        });

        if (!value || !this.mockTempData) {
          this.$message({
            type: 'warning',
            message: '描述或模板内容不能为空',
          });
          return;
        }

        const data = {
          methodID: this.mockData.selectedValue.methodID,
          dataDesc: value,
          mockData: this.mockTempData,
        };

        const response = await callApi("api/mock/create_mock_data", data);

        const refreshRes = await this.getMockData('method', this.mockData.selectedValue.methodID);

        this.$message({
          type: 'success',
          message: '提交保存模板: ' + value + '，并刷新',
        });
      } catch (error) {
        console.error('createMockData error:', error);
        this.$message({
          type: 'error',
          message: '提交保存模板失败' + error,
        });
      }
    },
    async creditRemark() {
      try {
        const {value} = await this.$prompt('备注标题', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        });
        // console.log("creditRemark::data::", value, this.mockData.selectedValue.methodID, this.mockData.methodRemarkData);
        if (!value || !this.mockData.selectedValue.methodID || !this.mockData.methodRemarkData) {
          this.$message({
            type: 'warning',
            message: '方法、标题、备注不能为空',
          });
          return;
        }

        const data = {
          methodID: this.mockData.selectedValue.methodID,
          title: value,
          remarkData: this.mockData.methodRemarkData,
        };

        const response = await callApi("api/mock/create_remark", data);

        const refreshRes = await this.getMockData('method', this.mockData.selectedValue.methodID);

        this.$message({
          type: 'success',
          message: '提交保存模板: ' + value,
        });
      } catch (error) {
        console.error('createMockData error:', error);
        this.$message({
          type: 'error',
          message: '提交保存模板失败',
        });
      }
    },
    // 新增mock场景
    createMockScene() {
      this.mockData.updateForm = {};
      this.changIsShow('dialogMockScene');
    },
    // 编辑mock场景
    editMockScene(row = {}) {
      this.mockData.updateForm = {...row};
      this.changIsShow('dialogMockScene');
    },
    // 应用mock场景
    async executeMockScene(row) {
      const params = this.mockData.updateForm = {...row};
      const response = await callApi("api/mock/scene/execute", params)
      // console.log("applyMockScene:response", response);
      const executeApplyRes = JSON.stringify(response, null, 2);
      this.$message({
        showClose: true,
        duration: 0,
        message: executeApplyRes,
      });
    },
    // 更新mock场景
    async changeMockScene() {
      this.changIsShow('dialogMockScene');
      let response;
      console.log("updateMockScene:params::updateForm::", this.mockData.updateForm);
      if (!this.mockData.updateForm.scene_id) {
        this.mockData.updateForm.group = this.mockData.selectedValue.groupID;
        const params = this.mockData.updateForm;
        console.log("updateMockScene:params::create", params);
        response = await callApi("api/mock/scene/create", params)
      } else {
        const params = this.mockData.updateForm;
        console.log("updateMockScene:params::update", params);
        response = await callApi("api/mock/scene/update", params)
      }

      console.log("updateMockScene:response", response);
      const sceneUpdateRes = JSON.stringify(response, null, 2);
      this.$message({
        message: sceneUpdateRes,
      });
    },
    async refreshMock() {
      callApi("api/mock/refresh").then(res => {
        // 弹出通知框
        this.$notify({
          title: '刷新mock数据结果',
          message: res
        })
      })
    },
    updateMockDataInput(value) {
      const selectedTemplate = this.mockData.param.mockTempList.find(temp => temp.data_id === value);
      if (selectedTemplate) {
        // this.mockTempData = JSON.stringify(selectedTemplate.mock_data, null, 2);
        this.mockTempData = selectedTemplate.mock_data;
      }
    },
    copyToClipboard(value) {
      copyToClipboard(value, this.$message);
    },
  },
}
