import { callApi } from "../api/http.js";

export default {
  name: 'user-data-collect',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
  <div style="padding: 20px; background: linear-gradient(180deg, #f6f8fc 0%, #eef3fb 100%); border-radius: 24px;">
    <el-card shadow="hover" style="max-width: 960px; margin: 0 auto; border-radius: 24px; border: 1px solid #e6ecf5; overflow: hidden;">
      <div style="padding: 8px 8px 24px;">
        <div style="margin-bottom: 24px; padding: 24px; border-radius: 20px; background: linear-gradient(135deg, #0f766e 0%, #0f766e 35%, #14b8a6 100%); color: #ffffff; box-shadow: 0 18px 40px rgba(15, 118, 110, 0.24);">
          <div style="display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; flex-wrap: wrap;">
            <div>
              <div style="font-size: 13px; letter-spacing: 1px; opacity: 0.8; margin-bottom: 8px;">DATA CLEAN CENTER</div>
              <div style="font-size: 28px; font-weight: 700; margin-bottom: 10px;">用户数据清理面板</div>
              <div style="font-size: 14px; line-height: 1.8; opacity: 0.92; max-width: 560px;">
                保留原有清除逻辑，仅优化页面视觉与操作分区。适合联调前快速清理用户数据，避免状态污染。
              </div>
            </div>
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
              <div style="min-width: 136px; padding: 14px 16px; border-radius: 16px; background: rgba(255,255,255,0.16); backdrop-filter: blur(8px);">
                <div style="font-size: 12px; opacity: 0.8; margin-bottom: 6px;">当前环境</div>
                <div style="font-size: 18px; font-weight: 700;">{{ selectedEnv }}</div>
              </div>
              <div style="min-width: 136px; padding: 14px 16px; border-radius: 16px; background: rgba(255,255,255,0.16); backdrop-filter: blur(8px);">
                <div style="font-size: 12px; opacity: 0.8; margin-bottom: 6px;">已选项目</div>
                <div style="font-size: 18px; font-weight: 700;">{{ selectedDelItems.length }}</div>
              </div>
            </div>
          </div>
        </div>

        <el-form label-position="top">
          <el-row :gutter="20">
            <el-col :xs="24" :md="10">
              <div style="height: 100%; padding: 20px; border-radius: 20px; background: linear-gradient(180deg, #ffffff 0%, #f7fbfb 100%); border: 1px solid #d8eeea;">
                <div style="margin-bottom: 18px;">
                  <div style="font-size: 18px; font-weight: 700; color: #1f2937; margin-bottom: 6px;">查询条件</div>
                  <div style="font-size: 13px; color: #6b7280; line-height: 1.7;">输入手机号并发起清理，下面可选择需要删除的数据范围。</div>
                </div>

                <el-form-item label="手机号">
                  <el-input
                    class="input_box"
                    type="text"
                    id="delMobile"
                    placeholder="用户手机号明文"
                    v-model.trim="delMobile"
                    clearable
                  />
                </el-form-item>

                <div style="padding: 14px 16px; border-radius: 16px; background: #f0fdfa; border: 1px solid #99f6e4; color: #0f766e; font-size: 13px; line-height: 1.8;">
                  建议仅勾选本次联调需要清理的数据，避免误删过多上下文信息。
                </div>

                <div style="margin-top: 18px; display: flex; justify-content: flex-end;">
                  <el-button
                    class="submit-button"
                    id="clearBtn"
                    type="primary"
                    @click="clear"
                    style="min-width: 160px; height: 44px; border-radius: 14px; box-shadow: 0 12px 26px rgba(20, 184, 166, 0.24);"
                  >
                    提交清除
                  </el-button>
                </div>
              </div>
            </el-col>

            <el-col :xs="24" :md="14">
              <div style="height: 100%; padding: 20px; border-radius: 20px; background: #f8fbff; border: 1px solid #dbe7f5; box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);">
                <div style="margin-bottom: 18px;">
                  <div style="font-size: 18px; font-weight: 700; color: #1f2937; margin-bottom: 6px;">清理项选择</div>
                  <div style="font-size: 13px; color: #6b7280; line-height: 1.7;">所有选项与原有能力保持一致，只优化成更易读的卡片式多选列表。</div>
                </div>

                <el-checkbox-group v-model="selectedDelItems">
                  <el-row :gutter="14">
                    <el-col :xs="24" :sm="12" v-for="item in delItems" :key="item.value" style="margin-bottom: 14px;">
                      <div :title="item.title" style="height: 100%; padding: 14px 16px; border-radius: 16px; background: #ffffff; border: 1px solid #e5edf8; box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);">
                        <el-checkbox :label="item.value" style="width: 100%; margin-right: 0;">
                          <div style="display: flex; flex-direction: column; gap: 6px;">
                            <span style="font-size: 14px; font-weight: 700; color: #1f2937;">{{ item.label }}</span>
                            <span style="font-size: 12px; line-height: 1.7; color: #6b7280; white-space: normal;">{{ item.title }}</span>
                          </div>
                        </el-checkbox>
                      </div>
                    </el-col>
                  </el-row>
                </el-checkbox-group>
              </div>
            </el-col>
          </el-row>

          <div style="margin-top: 20px; padding: 18px; border-radius: 20px; background: linear-gradient(180deg, #f7fcfb 0%, #eefaf7 100%); border: 1px solid #d8eeea; box-shadow: inset 0 1px 0 rgba(255,255,255,0.72);">
            <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 14px;">
              <div>
                <div style="font-size: 18px; font-weight: 700; color: #1f2937; margin-bottom: 6px;">清理结果</div>
                <div style="font-size: 13px; color: #6b7280;">接口返回内容将在此区域展示，便于核对本次清理是否成功。</div>
              </div>
              <div style="padding: 8px 12px; border-radius: 999px; background: #ccfbf1; color: #0f766e; font-size: 12px; border: 1px solid #99f6e4;">
                Response Output
              </div>
            </div>
            <div style="padding: 12px; border-radius: 16px; background: rgba(255,255,255,0.82); border: 1px solid #dfeeea;">
              <el-input
                type="textarea"
                :autosize="{ minRows: 8, maxRows: 40 }"
                placeholder="清除用户信息结果"
                v-model="delUserInfoRes"
                style="width: 100%;"
              >
              </el-input>
            </div>
          </div>
        </el-form>
      </div>
    </el-card>
  </div>
  `,
  data() {
    return {
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
