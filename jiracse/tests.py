import datetime
from jira import JIRA
from django.test import TestCase
# Create your tests here.

def jiralogin():
    """
    jira 账户登录
    :return:
    """
    options = {
        'server': 'https://easystack.atlassian.net/',
        'verify': False
    }

    jira = JIRA(options, basic_auth=('wenwei.hao@easystack.cn', 'H4SsUoaJgowMnXac9zw01ED9'))
    # projects = jira.projects()
    return jira


def jirasql(sqlstr):
    """
    jira sql 查询
    :return: 返回jira sq了查询下结果
    """
    # maxResults=xx最大 也只有100  需要取消该值验证
    jira = jiralogin()
    jirasqlresult = jira.search_issues(sqlstr, maxResults=False)

    print(jirasqlresult)

def dicsum():
    d={
       'a':2,
        'd':3,
    }
    print(sum(d.values()))
from jiracse.views import CseInfo
def cseresult(csekey):
    """
    根据sql 结果返回基础信息
    :return: 返回的是与当前cse key 相关的子case 信息
            返回当前cse 本身的基础信息：
                客户名称：
                项目名称：
                维保：
    """
    jira = jiralogin()
    # csekey = CseInfo.getcsekey(self,csekey)
    cseinfo = jira.issue(csekey)
    cse = {
        'projectname':cseinfo.fields.customfield_11190,
        'customername':''.join(cseinfo.fields.customfield_11191),
        'fullname':cseinfo.fields.summary,
        'describe':cseinfo.fields.description,
    }
    return cse



# import requests
#
# url = 'http:127.0.0.1:8100/api/testinfo'
# data = {'data',2}
# h = requests.post(url,json=data)
# print(h.text)
cseresult('ECSDESK-18971')
# if __name__ == '__main__':
#     # sqlstr = '"Epic Link"  in (CSE-1589)'
#     # jirasql(sqlstr)
#     # dicsum()
#     # print(datetime.date.today().year)
#     # reyear=str(datetime.date.today().year)
#     # print(reyear+"-01-")
#     # lis = [0]*12
#     # print(lis)
#     result = cseresult('ECSDESK-18971')
#     print(result)


