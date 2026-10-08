# webTools


> 项目结构说明：
>
> https://ccnfgxrpun87.feishu.cn/wiki/MRcDwWkbtisnJ3kF4R6cuGdHnZe

配置系统属性环境变量：

```
 TEST_ENV=local
```

安装依赖包：

```
pip install -r requirements.txt
```


### 启动web项目：（非必要）

命令行执行：

```
python manage.py runserver
```



### 启动自动化测试：

执行pytestAutoTest/case/run_case.py文件

在该文件中指定需执行的用例，如：

```
run(test_case_path="app/flow_case/test_0_credit.py::TestCredit", test_case_name="test_credit_success")
```

