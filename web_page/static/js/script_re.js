document.addEventListener('DOMContentLoaded', () => {
    window.vueApp = new Vue({
        // delimiters: ['[[', ']]'],
        el: '#app',
        created() {
            console.log('Vue实例已创建');
        },
        data: {
            isNavShow: false,
            isUserInfoShow: false,
            isChannelShow: false,
            isProductChannelShow: false,
            isRandomUserInfoShow: false,
            isFundCallbackShow: false,
            isRiskShow: false,
            isCreateUserInfoShow: false,
            isChannelJsonShow: true,
            isDelUserInfoShow: false,
            isCreateUserShow: false,
            isTestBarShow: false,
            isMockBarShow: false,
            isUpdatePilotShow: false,
            isGetLandUrlShow: false,
            isFeedBackShow:false,

            EnvOptions: ['BM_SIT', 'DEV'],
            selectedEnv: "BM_SIT",
        },
        methods: {

            // 选择环境
            selectEnvironment(environmentId) {
                console.log("environmentId", environmentId);
                this.selectedEnv = environmentId;
                console.log("selectedEnv", this.selectedEnv);
            },
            // 实现点击切换显示隐藏
            changIsShow(tag) {
                this[tag] = !this[tag];
            },
        },
        components: {},
        mounted() {
        },
        watch: {},
    });
});