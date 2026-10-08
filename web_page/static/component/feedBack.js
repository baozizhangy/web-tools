import { callApi } from '../api/http.js'

export default {
  name: 'feed-back',
  props: {
    selectedEnv: {
      type: String,
      required: true
    },
  },
  template: `
    <div>
      <div>
        <label >生成的用户个数：
        <input  class="input_box" v-model="numusers" placeholder="默认1个用户">
        </input>
        </label>    
        <label >问题的个数：
        <input class="input_box"  v-model="numquestionsperuser" placeholder="默认1个问题">
        </input>
        </label>
        <label>选择机构产品：
          <el-select v-model:is=productname filterable clearable placeholder="默认随机生成" >
          <el-option v-for="option in quesitonfundtypes" :key="option.value" :label="option.value"
            :value="option.value"></el-option>
          </el-select>
        </label>
        <label>选择问题类型：
        <el-select id="eventCodeSelect" v-model="questiontype"  filterable clearable placeholder="默认随机生成">
          <el-option v-for="option in questiontypes" :key="option.value" :label="option.value"
            :value="option.value"></el-option>
        </el-select>
        </label>
        <el-button class="submit-button" id="submitCreditBtn" @click="generateProblemFeedBack" >
          <span>生成</span>
        </el-button><br>
      </div>
      <div>
        <label>生成结果:</label>
        <textarea class="output-box" ref="QuestionFeedBackextarea" v-model="QuestionFeedBackDataRes"
          placeholder="生成结果"></textarea>
      </div>
    </div>
  `,
  data() {
    return {
      // 问题反馈
      quesitonfundtypes:[],//用于存放选项的数据
      QuestionFeedBackDataRes:"",
      questiontype:null,
      productname:null,
      questiontypes:[
        {value:'还款问题'},
        {value:"申请问题"},
        {value:"会员问题"},
        {value:"违规举报"},
        {value:"其他问题"},
        {value:"提现问题"},
      ],
      numusers:null,
      numquestionsperuser:null,
    };
  },
  computed: {
  },
  methods: {
    //问题反馈提交
    async generateProblemFeedBack(){
        const data = {
            env: this.selectedEnv, //获取环境变量,
            numusers:this.numusers,
            numquestionsperuser:this.numquestionsperuser,
            questiontype:this.questiontype,
            productname:this.productname
        };
        try {
            this.QuestionFeedBackDataRes = null;
            this.errorMessage = null;
            // if (!data.env || !data.mobile || !data.pilotcode) {
            //     throw new Error("缺少必填参数:请确保已选择环境、输入手机号、选择对应节点");
            // }
            const response = await fetch("api/generate_help_submit_api", {
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
            this.QuestionFeedBackDataRes = JSON.stringify(responseData, null, 2);
            // 调整 textarea 高度
            this.$nextTick(() => {
                this.adjustTextareaHeight('QuestionFeedBackextarea');
            });

        } catch (error) {
            console.error("Error querying codes", error.message);
            this.errorMessage = error.message || "更新过程中出现错误，请稍后重试";
            this.QuestionFeedBackDataRes = this.errorMessage;
        } finally {
        }
    },
    //问题反馈机构产品获取
    async getFundQuestionType() {
                const env = this.selectedEnv; // 获取环境值

                if (!env) {
                    console.error('The environment value is missing or undefined');
                    return;
                }

                const fundurl = `api/get_fund_question_product_type?env=${encodeURIComponent(env)}`;

                try {
                    const response = await fetch(fundurl); // 发起 GET 请求
                    const data = await response.json();
                    console.log("fundType---1",data.data); // 处理返回的数据
                    this.quesitonfundtypes = data.data
                } catch (error) {
                    console.error('Error fetching data:', error);
                }
            },
  },
  mounted() {
    this.getFundQuestionType();
  }
}
