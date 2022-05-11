#!/usr/bin python3
# -*- encoding: utf-8 -*-
# @Author : hww
# @File : updatedb.py
# @Time : 2022/5/9 15:13
from .models import TbCse,TbEsdesk
import yaml,os,json
from jira import JIRA

class CseInfo:
    def __init__(self):
        pass
    @staticmethod
    def readconfig(filepath):
        # print(settings.SITE_ROOT)
        with open(filepath, 'r', encoding='utf-8') as f:
            jiradata = yaml.load(f, Loader=yaml.FullLoader)
            return jiradata
    @classmethod
    def jiralogin(cls):
        """
        jira 账户登录
        :return:
        """
        module_dir = os.path.dirname(__file__)
        # print(module_dir)
        filepath = os.path.join(module_dir, 'config.yaml')
        jirafile = CseInfo.readconfig(filepath)
        options = {
            'server': jirafile['url'],
            'verify': False
        }
        jira = JIRA(options, basic_auth=(jirafile['name'], jirafile['jiarkey']))
        return jira
    @classmethod
    def jirasql(cls,sqlstr):
        """
        jira sql 查询
        :return: 返回jira sq了查询下结果
        """
        i = 0

        # print("访问次数",i =+ 1)
        jira = CseInfo.jiralogin()
        # maxResults=xx最大 也只有100  需要取消该值验证
        jirasqlresult = jira.search_issues(sqlstr, maxResults=False)
        return jirasqlresult
cseinfoinit = CseInfo()
def updatecsetotals():
    csetotalsql ='project in (CustomerEnvironment) AND issuetype  = Epic AND status != Done '
    csetotalresult = cseinfoinit.jirasql(csetotalsql)
    resultdata=[]
    for i in csetotalresult:
        data = {}
        data['cseid'] = i.key
        tbcseid = TbCse.objects.get(cseid=data['cseid'])
        if tbcseid.exists():
            break
        #单条数据更新动作暂不考虑，不考虑从django侧主动更新
        else:
            data['csename'] = i.fields.customfield_10008
            data['csestatus'] = i.fields.status.name
            data['customername'] = i.fields.customfield_11191
            data['projectname'] = i.fields.customfield_11190
            data['fullname'] = i.fields.summary
            try:
                data['version'] = i.fields.fixVersions[0].name
            except:
                print(i.key)
            data['maintenancedate'] = i.fields.customfield_11221
            data['environmenttype'] = i.fields.customfield_11220.value
            resultdata.append(data)
            tbcse = TbCse(cseid=data['cseid'],csename=data['csename'],csestatus=data['csestatus'],customername=data['customername'],
                          projectname=data['projectname'],fullname=data['fullname'],
                          version=data['version'],maintenancedate=data['maintenancedate'],environmenttype=data['environmenttype'])
            tbcse.save()

