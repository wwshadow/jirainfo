#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import random
import re

import json
import requests
from jira import JIRA
import jira.client
import urllib3
from .views import CseInfo
urllib3.disable_warnings()
import sys
sys.setrecursionlimit(9000000)

def FillTime(Authorization,tompetime,esdeskid,workerId, is_autofill=False):
    cseinfo = CseInfo()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Authorization': Authorization,
        'Content-Type': 'application/json'
    }
    if is_autofill:
        startofweek_jql = 'type in (Incident, Problem, "Service Request", Change, Task) ' \
                          'AND assignee = %s  AND createdDate >= startOfWeek(0) ' % workerId

        sqls = cseinfo.search_issues(startofweek_jql, maxResults=False)
        for i in range(len(sqls)):
            # print(len(sqls))
            ECSDESK_infos = jira.issue(sqls[i].key)
            try:
                infofields_time = ECSDESK_infos.fields.timespent
                if infofields_time == None:
                    hours = 0
            except:
                # infofields_time = '0h'
                hours = 0
            # global hours
            originTaskIDs = ECSDESK_infos.id
            createtime = (ECSDESK_infos.fields.created).split("+", 1)[0]
            tempohour = [8, 8.5]
            # 工时选择范围，单位小时
            secend = 3600

            if hours == 0:
                timechoces = random.choice(tempohour)
                rel_temposecond = timechoces * secend
                data = {
                    'attributes': {},
                    # billableSeconds 工时 单位h
                    'billableSeconds': rel_temposecond,
                    # originTaskId esdesk jira id
                    'originTaskId': originTaskIDs,
                    'remainingEstimate': 0,
                    # esdesk创建时间
                    'started': createtime,
                    # 将填写得工时时间
                    'timeSpentSeconds': rel_temposecond,
                    # 用户id
                    'workerId': workerId
                }
                try:
                    result = requests.post("https://app.tempo.io/rest/tempo-timesheets/4/worklogs/", headers=headers,
                                           data=json.dumps(data))
                    # 上线8小时限制 已经不存在
                    # hours = data.get('billableSeconds')
                    if result.status_code == 400:
                        #自动需要对时间进行拼接
                        time2 = createtime.replace("T", " ")
                        time3 = createtime.split('.', 2)[1]
                        times = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M:%S." + time3)
                        a = [-1, 0, 1]
                        for i in range(1, 2):
                            timeAfter = times + datetime.timedelta(days=random.choice(a))
                            createtimes = timeAfter
                            r_createtimes = datetime.datetime.strftime(createtimes, "%Y-%m-%d %H:%M:%S." + time3)
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
                                'workerId': workerId
                            }
                            result = requests.post("https://app.tempo.io/rest/tempo-timesheets/4/worklogs/",
                                                   headers=headers,
                                                   data=json.dumps(data))
                            # print(data.started, data.originTaskId,timechoces)
                            hours = data.get('billableSeconds')
                            if result.status_code == 200:
                                return result.text
                    if result.status_code == 401:
                        print("认证失效，重新获取")
                        return result.text
                except Exception as e:
                    return result.text
    else:
        ECSDESK_infos = jira.issue(esdeskid)
        createtime = (ECSDESK_infos.fields.created).split("+", 1)[0]
        originTaskIDs = ECSDESK_infos.id
        data = {
            'attributes': {},
            # billableSeconds 工时 单位h
            'billableSeconds': tompetime,
            # originTaskId esdesk jira id
            'originTaskId': originTaskIDs,
            'remainingEstimate': 0,
            # esdesk创建时间
            'started': createtime,
            # 将填写得工时时间
            'timeSpentSeconds': tompetime,
            # 用户id
            'workerId': workerId
        }
        try:
            result = requests.post("https://app.tempo.io/rest/tempo-timesheets/4/worklogs/", headers=headers,
                                   data=json.dumps(data))
            if result.status_code == 200:
                print("完成")
                return result

            if result.status_code == 400:
                print(result)
                return result
            if result.status_code == 401:
                print(result,"认证失败")
                return result
        except Exception as e:
            print(e)






if __name__ == '__main__':
    tompetime = '70'
    esdeskid = ''
    workerId = ''
    Authorization = "xxx"
    is_autofill = True
    FillTime(Authorization,tompetime,esdeskid,workerId,is_autofill)

