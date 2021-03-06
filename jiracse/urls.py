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
    path('csetotal', views.UpdateCsetotalView.as_view()),
    path('getcsetotal', views.GetCsetotalView.as_view()),
    path('csemonth/', views.CseMonthView.as_view()),
    path('usercase/', views.UserCaseView.as_view()),
    path('filltompe/', views.FilltempoView.as_view()),
    path('ecsbymonth', views.EcsByMonthView.as_view()),
    path('selectcse/', views.SelectCseView.as_view()),
    path('ecsbymonthpage', views.EcsByMonthPageView.as_view()),
    path('jirauser', views.JiraUserloginView.as_view()),
    path('estotp/', views.TotpView.as_view()),
    path('esdesk/', views.EsdeskView.as_view()),


]