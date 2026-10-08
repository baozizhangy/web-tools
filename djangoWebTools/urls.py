"""
URL configuration for djangoWebTools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os

from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from djangoWebTools.views import (
    init_plan, repay_loan, loan_compensation, trigger_xxl_job, bm_credit_apply, bm_credit_order, bm_query_order, query_user,
    bm_repay_order, bm_query_repay_order, bm_query_repay_result, bm_repay_trail_order, bm_update_mock, bm_get_h5_url,
    h5_bind_card_scene, h5_draw_submit_scene, h5_repay_scene, h5_coupon_receive, bm_offline_oak_pay
)

from django.views.generic import TemplateView
from django.views.static import serve
from djangoWebTools.tools.bm_tools.navigation_handle import get_navigation_config, create_navigation_config


urlpatterns = [
    path('', TemplateView.as_view(template_name='index_new.html'), name='index'),
    # path('page/re', TemplateView.as_view(template_name='index.html'), name='index'),
    # path('page/new', TemplateView.as_view(template_name='index_new.html'), name='index'),
    # 初始化账单状态
    path('api/init_plan', init_plan, name='init_plan'),
    # 借据变更为还款成功
    path('api/repay_loan', repay_loan, name='repay_loan'),
    # 借据代偿流程
    path('api/loan_compensation', loan_compensation, name='loan_compensation'),
    # 请求xxl-job执行脚本
    path('api/trigger_xxl_job', trigger_xxl_job, name='trigger_xxl_job'),
    # 助贷发起授信
    path('api/credit_apply', bm_credit_apply, name='bm_credit_apply'),
    # 助贷发起创单
    path('api/credit_order', bm_credit_order, name='bm_credit_order'),
    # 查询订单状态，并触发放款脚本
    path('api/query_order', bm_query_order, name='bm_query_order'),
    path('api/nav/get', get_navigation_config, name='get_navigation_config'),
    path('api/nav/add', create_navigation_config, name='create_navigation_config'),
    path('admin/', admin.site.urls),
    path('api/query_user', query_user, name='query_user'),
    path('api/query_repay_order', bm_query_repay_order, name='bm_query_repay_order'),
    path('api/query_repay_result', bm_query_repay_result, name='bm_query_repay_result'),
    path('api/bm_repay_order', bm_repay_order, name='bm_repay_order'),
    path('api/bm_repay_trail_order', bm_repay_trail_order, name='bm_repay_trail_order'),
    path('api/bm_update_mock', bm_update_mock, name='bm_update_mock'),
    path('api/bm_get_h5_url', bm_get_h5_url, name='bm_get_h5_url'),
    path('api/h5/scene/bind_card', h5_bind_card_scene, name='h5_bind_card_scene'),
    path('api/h5/scene/draw_submit', h5_draw_submit_scene, name='h5_draw_submit_scene'),
    path('api/h5/scene/repay', h5_repay_scene, name='h5_repay_scene'),
    path('api/h5/scene/coupon_receive', h5_coupon_receive, name='h5_coupon_receive'),
    # 橡树线下还款接口
    path('api/offline_oak_pay', bm_offline_oak_pay, name='bm_offline_oak_pay'),
]

urlpatterns += [
    re_path(r'allure/(?P<path>.*)$', serve, {"document_root": os.path.join(settings.BASE_DIR, 'reports', 'allure-reports')}),
    re_path(r'static/(?P<path>.*)$', serve, {"document_root": 'web_page/static'}),
]
