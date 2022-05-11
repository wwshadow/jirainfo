#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import random
import re

import json
import requests
from jira import JIRA
import jira.client
import getpass
import urllib3

urllib3.disable_warnings()
import sys

sys.setrecursionlimit(9000000)
options = {
    'server': 'https://easystack.atlassian.net/',
    'verify': False
}

jira = JIRA(options, basic_auth=('wenwei.hao@easystack.cn', 'JIDgL6gKisxURPPKVwnh9A1C'))
#https://id.atlassian.com/manage-profile/security/api-tokens
projects = jira.projects()
workerID = '5f812189287870006a5c85b4'
# jira 搜索切换到sql语句，获取当前用户ID
Authorization = 'Tempo-Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJpZGVudGl0eSIsInRlbXBvX2NvbnRleHQiOiJ7XCJ0ZW5hbnRcIjoge1wiaWRcIjogXCI3NzM4NGY5Yy0yOGYwLTRiYTEtODdkOS1lZWQyNDUyODA4ZWZcIiwgXCJiYXNlVXJsXCI6IFwiaHR0cHM6XC9cL2Vhc3lzdGFjay5hdGxhc3NpYW4ubmV0XCIsIFwicmVsYXRlZFRlbmFudHNcIjogW1wiaW8udGVtcG8uamlyYVwiLCBcImlzLm9yaWdvLmppcmEudGVtcG8tcGx1Z2luXCJdLCBcInJlbGF0ZWRUZW5hbnRVdWlkc1wiOiBbXCI3NzM4NGY5Yy0yOGYwLTRiYTEtODdkOS1lZWQyNDUyODA4ZWZcIiwgXCJlZmE2ZDkzMS04ZjFlLTQ1OTYtYmFmMy1lOWExM2Y4YzExMjRcIl0sIFwic2VuTnVtYmVyXCI6IFwiU0VOLTM1MjUzNzVcIiwgXCJtaWdyYXRlZFwiOiBmYWxzZSwgXCJjcmVhdGVkXCI6IFwiMjAyMS0wMy0xMFQxMjowNjo0Ni45OTExNDQrMDA6MDBcIiwgXCJldmFsdWF0aW9uTGljZW5zZXNcIjoge1wiaXMub3JpZ28uamlyYS50ZW1wby1wbHVnaW5cIjogZmFsc2UsIFwiaW8udGVtcG8uamlyYVwiOiBmYWxzZX19LCBcInVzZXJcIjoge1wiaWRcIjogXCI2NjYxOWZhMi01OTliLTRlOGUtYmY5Mi0zYTBmOGE4MzhmOTZcIiwgXCJhY2NvdW50SWRcIjogXCI1ZjgxMjE4OTI4Nzg3MDAwNmE1Yzg1YjRcIn0sIFwib3JpZ2luXCI6IFwiamlyYVwifSIsImV4cCI6MTY1MTIyOTgzMSwiaWF0IjoxNjUxMjI4OTMxfQ.8nSWcBeYI7kHziW7-zsEN_3Xp9DaUoM1QrX9gJVhwaE'
# jira,应用-tempo F12 XHR 获取如下request信息：
# approval-statuses?numberOfPeriods=3&accountId=5f43585b3236070038c11d4   中 requestheader中找到 Authorization，复制value即可。


def FillTime():
    '''上周工作情况'''

    new_time_jql = 'project in ("Service Desk", "EasyStack Customer Support") AND type in (Incident, Problem, "Service Request",Change,Task) ' \
                   ' AND assignee = %s ' \
                   ' AND createdDate >=2022-04-25 and createdDate <=2022-04-29' %workerID
#需要按需求，修改时间

    sqls = jira_sql(new_time_jql)
    timelists = []
    global originTaskIDs
    for i in range(len(sqls)):
        # print(len(sqls))
        ECSDESK_infos = jira.issue(sqls[i].key)
        try:
            infofields_time = ECSDESK_infos.fields.timetracking.timeSpent
        except:
            infofields_time = '0h'

        originTaskIDs = ECSDESK_infos.id
        createtime = (ECSDESK_infos.fields.created).split("+", 1)[0]
        total_hour = daytohours(infofields_time, originTaskIDs, createtime)

        print(ECSDESK_infos, total_hour, createtime.split("T")[0])


def daytohours(infofields_time,originTaskIDs,createtime):
    global hours
    tempohour = [8,]
    #9, 9.25, 10
    #工时选择范围，单位小时
    secend = 3600
    # if re.search("[d]", infofields_time) and re.search("[h]", infofields_time):
    if 'd' in infofields_time and "h" in infofields_time:

        hours = 8*int((re.findall("[\d+]",infofields_time))[0]) + int(re.findall("[\d+]", infofields_time)[1])
    # if re.search("[d]", infofields_time) :
    if 'd' in infofields_time and "h" not in infofields_time:
        hours = 8*int((re.findall("[\d+]",infofields_time))[0])
    # if re.search("[h]", infofields_time) :
    if 'h' in infofields_time and "d" not in infofields_time:
        hours = int(re.findall("[\d+]", infofields_time)[0])
        if hours == 0:
            # pass
            # originTaskIDs = originTaskIDs
            timechoces = random.choice(tempohour)
            rel_temposecond = timechoces * secend
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                'Authorization': Authorization,
                'Content-Type': 'application/json'
            }
            data = {
                'attributes': {},
                'billableSeconds': rel_temposecond,
                'originTaskId': originTaskIDs,
                'remainingEstimate': 0,
                'started': createtime,
                'timeSpentSeconds': rel_temposecond,
                'workerId': workerID
            }
            try:
                result = requests.post("https://app.tempo.io/rest/tempo-timesheets/4/worklogs/", headers=headers, data= json.dumps(data))
                #上线8小时限制 已经不存在
                # hours = data.get('billableSeconds')
                if result.status_code == 400:

                    time2 = createtime.replace("T", " ")
                    time3 = createtime.split('.', 2)[1]
                    times = datetime.datetime.strptime(time2,"%Y-%m-%d %H:%M:%S."+time3)
                    a = [-1, 0,]
                    for i in range(1):
                        timeAfter = times + datetime.timedelta(days=random.choice(a))
                        createtimes = timeAfter
                        r_createtimes = datetime.datetime.strftime(createtimes, "%Y-%m-%d %H:%M:%S."+time3)
                        timechoces = random.choice(tempohour)
                        # isworkday(r_createtimes)
                        rel_temposecond = timechoces * secend
                        data = {
                            'attributes': {},
                            'billableSeconds': rel_temposecond,
                            'originTaskId': originTaskIDs,
                            'remainingEstimate': 0,
                            'started': r_createtimes,
                            'timeSpentSeconds': rel_temposecond,
                            'workerId': workerID
                        }
                        result = requests.post("https://app.tempo.io/rest/tempo-timesheets/4/worklogs/", headers=headers,
                                               data=json.dumps(data))
                        # print(data.started, data.originTaskId,timechoces)
                        houinfofields_timers = data.get('billableSeconds')
                        if result.status_code == 200:
                            hours = data.get('billableSeconds')
                            break
                if result.status_code == 401:
                    print("认证失效，重新获取")
                    exit(1)
            except Exception as e:
                print(e)
        elif hours < 8:
            pass
    return result


def sumOfList(list, size):
    if (size == 0):
        return 0
    else:
        return list[size - 1] + sumOfList(list, size - 1)


def jira_sql(jql):
    return jira.search_issues(jql, maxResults=False)  # maxResults=xx最大 也只有100  需要取消该值验证


if __name__ == '__main__':
    FillTime()

