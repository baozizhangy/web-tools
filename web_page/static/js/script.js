


document.addEventListener('DOMContentLoaded', () => {
    window.vueApp = new Vue({
        el: '#app',
        data: {
            EnvOptions: ['BM_SIT', 'DEV'],
            selectedEnv: 'BM_SIT',
            components: [
                {name: 'navigation-menu', label: '导航', showKey: 'isNavShow'},
                {name: 'queryUserInfo', label: '查询用户信息', showKey: 'isUserInfoShow'},
                {name: 'InitLoan', label: '助贷订单初始化', showKey: 'isLoanShow'},
                {name: 'apply_info', label: '创建授信用户', showKey: 'isBmCreditApplyShow'},
                {name: 'query-order', label: '查询放款状态', showKey: 'isQueryOrderShow'},
                {name: 'credit-apply', label: '用户授信', showKey: 'isCreditApplyShow'},
                {name: 'credit-order', label: '用户借款', showKey: 'isCreditOrderShow'},
                {name: 'repay-order', label: '还款', showKey: 'isRepayOrderShow'},
                {name:'update-mock',label: 'mock数据修改',showKey:'isUpdateMockShow'},
                {name:'get-url',label:'获取H5链接',showKey:'isGetUrlShow'},
                {name:'bind-card-submit',label:'H5绑卡',showKey:'isBindCardShow'},
            ],
            // 静态定义每个组件的显示状态
            isNavShow: true,
            isCreateUserInfoShow: false,
            isUserInfoShow: false,
            DelUserInfoShow: false,
            isChannelShow: false,
            isRandomUserInfoShow: false,
            isFundCallbackShow: false,
            isRiskShow: false,
            isMockBarShow: false,
            isUpdatePilotShow: false,
            isGetLandUrlShow: false,
            isLoanShow: false,
            isBmCreditApplyShow:false,
            isQueryOrderShow:false,
            isCreditApplyShow:false,
            isCreditOrderShow:false,
            isRepayOrderShow:false,
            isUpdateMockShow:false,
            isGetUrlShow:false,
            isBindCardShow:false,

        },
        methods: {
            selectEnvironment(environmentId) {
                this.selectedEnv = environmentId;
            },
            changIsShow(tag) {
                // 切换组件显示状态
                console.log(tag);
                this[tag] = !this[tag];
            },
        },
        created() {
            console.log('Vue实例已创建');
        },
    });
});
