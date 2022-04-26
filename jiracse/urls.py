#!/usr/bin python3
# -*- encoding: utf-8 -*-
# @Author : hww
# @File : urls.py
# @Time : 2022/3/18 10:44
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('cse/', views.CseDescribeView.as_view()),
    path('csetype/', views.CseTypeView.as_view()),
    path('csechild/', views.CseChildView.as_view()),
    path('csetotal',views.CsetotalView.as_view()),
    path('csemonth/', views.CseMonthView.as_view()),
    path('usercase/', views.UserCaseView.as_view()),
]