import datetime
import json
import os
# Create your views here.
from django.core.paginator import Paginator
from django.http import JsonResponse
from jira import JIRA
from rest_framework import serializers
from rest_framework.response import Response
import yaml
import sys
from rest_framework.views import APIView

from .serializer import TbjirauserSerializer

sys.setrecursionlimit(9000000)
import requests
requests.packages.urllib3.disable_warnings()
from .models import TbCse, TbEsdesk, TbJirauser
from django.core import serializers


filepath = os.path.join(os.path.dirname(__file__), 'config.yaml')
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

        jirafile = CseInfo.readconfig(filepath)
        options = {
            'server': jirafile['jira']['url'],
            'verify': False
        }

        jira = JIRA(options, basic_auth=(jirafile['jira']['name'], jirafile['jira']['jirakey']))
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

def localjirauser(jiraname,jirakey):
    jirafile = CseInfo.readconfig(filepath)
    options = {
        'server': jirafile['jira']['url'],
        'verify': False
    }
    jira = JIRA(options, basic_auth=(jiraname, jirakey))
    return jira

def jirausrresult(jiraname,jirakey):

    msg = "ok"

    try:
         globaljirauser =localjirauser(jiraname,jirakey)

         jirauser = TbJirauser.objects.filter(jiraname=jiraname)
         json_data = serializers.serialize('json', jirauser)
         ss=json.loads(json_data)
         print(ss[0]['fields']['jiraid'])
    except Exception as e:
        msg = "err"
        return msg
    if globaljirauser:

        return ss[0]['fields']['jiraid']


# def updatejirausr(jiraname,jirakey):
#     data = {'jiraname': jiraname,
#         'jirakey': jirakey}
#     getuser = TbJirauser.objects.filter(jiraname=data['jiraname'])
#     # getuser = TbjirauserSerializer(data=data['jiraname'])
#     if getuser:
#         globaljirauser = cseinfoinit.jiralogin(data)
#     else:
#         objSr = TbjirauserSerializer(data=data)
#         objSr.is_valid()
#         objSr.save()
#         globaljirauser = cseinfoinit.jiralogin(data)
#
#     msg = "ok"
#     try:
#         result = cseinfoinit.jiralogin(data)
#     except:
#         msg = "err"
#         return msg
#     if result:
#         return msg
def totploginresult(jiraemail,password):
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    }
    postData={
        "username": jiraemail,
        "password": password,
    }
    url = 'http://easytotp.easystack.io/api/login/'

    response = requests.post(url=url, headers=header, json=postData, allow_redirects=True)
    if response.status_code == 200:
        if json.loads(response.text)['code'] == 0:
             token = json.loads(response.text)['data']['token']
             return token
        else:
            msg = json.loads(response.text)['message']
            return msg

def totptokenresult(jiraemail,totppwd,*args):
    # totp_type =roller
    # customer,project,version,cse,totp_version,issue,auditor,reason,totp_type
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
    }

    logindata={
        "username": jiraemail,
        "password": totppwd,
    }

    url = 'http://easytotp.easystack.io/api/login/'
    response = requests.post(url=url, headers=header, json=logindata, allow_redirects=True)
    if response.status_code == 200:
        if json.loads(response.text)['code'] == 0:
            token = json.loads(response.text)['data']['token']
            cookies = token
            newdata = {
                'jiratotptoken': cookies
            }
            jiraemailsql = TbJirauser.objects.filter(jiraemail=jiraemail).first()
            sqlcookie = TbjirauserSerializer(jiraemailsql, data=newdata, partial=True)
            sqlcookie.is_valid()
            sqlcookie.save()
            return cookies
        else:
            msg = json.loads(response.text)['message']
            return msg

    url2 = 'http://easytotp.easystack.io/api/totp/totp/'
    # cookies = jiradata['jiracookie']
    # response = requests.post(url=url2, json=postData ,headers=header, cookies=cookies)
    # #再次申请
    # #验证成功结果
    # if json.loads(response.text)['code'] == 0:
    #     msg = json.loads(response.text)['data']
    #
    # else:
    #     msg = json.loads(response.text)['message']
    # return msg

def totpresult(jiraemail,Dynamicpwd,datas,totp_type,totp_version):
    datas["totp_version"] = totp_version
    datas["totp_type"] = totp_type
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
    }
    url = 'http://easytotp.easystack.io/api/totp/totp/'

    if Dynamicpwd:
        cookies = totptokenresult(jiraemail, Dynamicpwd)
        if cookies == "LDAP认证密码错误.":
            return cookies
        # else:
        #     pass
            # response = requests.post(url=url, json=postData, headers=header, cookies=cookies)
    else:
        # pass
        json_data = TbJirauser.objects.filter(jiraemail=jiraemail)
        serializerscookies = serializers.serialize('json', json_data, fields=('jiratotptoken'))
        cookies = json.loads(serializerscookies)[0]['fields']['jiratotptoken']
        # print(cookies)

    recookies= {"jwtToken":cookies}
    # 再次申请
    # 验证成功结果

    response = requests.post(url=url, json=datas, headers=header, cookies=recookies)
    if json.loads(response.text)['code'] == 0:

        msg = json.loads(response.text)['data']
    else:
        msg = json.loads(response.text)['message']
    return msg

def cseresult(csekey):
    """
    根据sql 结果返回基础信息
    :return: 返回的是与当前cse key 相关的子case 信息
            返回当前cse 本身的基础信息：
                客户名称：
                项目名称：
                维保：
    """
    jira = cseinfoinit.jiralogin()
    cseinfo = jira.issue(csekey)
    cse = {
        'projectname': cseinfo.fields.customfield_11190,
        'customername': ''.join(cseinfo.fields.customfield_11191),
        'fullname': cseinfo.fields.summary,
        'describe': cseinfo.fields.description,
    }
    return cse

def esdeskresult(esdeskid):
    """
    根据sql 结果返回基础信息
    :return: 返回的是与当前cse key 相关的子case 信息
            返回当前cse 本身的基础信息：
                客户名称：
                项目名称：
                维保：
    """
    # esdeskkey='ECSDESK-19814'
    jira = cseinfoinit.jiralogin()
    esdesk = jira.issue(esdeskid)
    cseid = esdesk.fields.customfield_10007
    cseinfo = cseresult(cseid)
    projectname =cseinfo['projectname']
    customername = cseinfo['customername']
    esdeskinfo = {
        'cseid': cseid,
        'project': projectname,
        'customer': customername,
        'reason': esdesk.fields.summary,
        'auditor': esdesk.fields.customfield_10400.displayName
    }
    return esdeskinfo

def userresult(jiraid):
    """
    根据sql 结果返回基础信息
    :return: 返回的是与当前cse key 相关的子case 信息
            返回当前cse 本身的基础信息：
                客户名称：
                项目名称：
                维保：
    """
    resultdata = TbJirauser.objects.filter(jiraid=jiraid)
    json_data = serializers.serialize('json', resultdata, fields=('jiraname','jiraemail','projectname','groups'))
    jirauserinfo = json.loads(json_data)
    # print(jirauserinfo[0]['fields'])
    return jirauserinfo[0]['fields']

def csetyperesult(csekey):
    """
    :return:返回改cse 下case 的统计情况
    """
    csechildtypesql = '"Epic Link"  in (%s)' % (csekey)

    #这个地方还可以在优化，自动获取所有类型
    issuetype = ['Change', 'Incident', 'Problem', 'Service request']
    case_type_num = {}
    jira_result = cseinfoinit.jirasql(csechildtypesql)
    for i in range(0, 4):
        #这里多次查询数据库较为耗时
        epiclink_type_sql = '"Epic Link"  in (%s) AND issuetype = "%s"' % (csekey, issuetype[i])
        lentype = len(cseinfoinit.jirasql(epiclink_type_sql))
        case_type_num[issuetype[i]] = lentype
    other_case_num = jira_result.total - sum(case_type_num.values())
    case_type_num['other'] = other_case_num
    datalist =[]
    for key in case_type_num:
        resultdata ={}
        resultdata['type']=key
        resultdata['value'] = case_type_num.get(key)
        datalist.append(resultdata)

    return datalist

def usercaseresult(userid):
    # if request.method =="GET":
    userlistsql = 'assignee in (%s) AND issuetype in (Problem, Incident, "Service Request",Change) AND Created >= startOfMonth(-1)' %userid
    # print(userlistsql)
    jira_result = cseinfoinit.jirasql(userlistsql)
    data = []
    for i in range(len(jira_result)):
        resdata = {}
        resdata['esdeskname'] = jira_result[i].fields.summary
        resdata['issueid']=jira_result[i].key
        resdata['issuetype'] = jira_result[i].fields.issuetype.name
        resdata['issuestatus'] = jira_result[i].fields.status.name
        resdata['createdata'] = jira_result[i].fields.created.split('T')[0]
        resdata['timespent'] = jira_result[i].fields.timespent
        data.append(resdata)
    return data

def csechildresult(csekey):
    csechildsql = '"Epic Link"  in (%s)' % (csekey)
    jira_result = cseinfoinit.jirasql(csechildsql)
    data = []
    for i in range(len(jira_result)):
        resdata = {}
        resdata['esdeskname'] = jira_result[i].fields.summary
        resdata['issueid'] = jira_result[i].key
        resdata['issuetype'] = jira_result[i].fields.issuetype.name
        resdata['issuestatus'] = jira_result[i].fields.status.name
        resdata['createdata'] = jira_result[i].fields.created.split('T')[0]
        data.append(resdata)
    return data
def ecsbymonthresult():
    """
    :param :ecsid
        :createdate
        :describe 摘要
        :creater 创建者
        :version 版本
        :status 状态
        assignee 经办人
        priority: 优先级
    :return:return ecs by this month
    """
    csechildsql = 'project in ("EasyStack Customer Support") AND createdDate  >= endOfMonth(-1)'
    jira_result = cseinfoinit.jirasql(csechildsql)
    data = []
    for i in range(len(jira_result)):
        resdata = {}
        resdata['ecsid'] = jira_result[i].key
        resdata['createdate']=jira_result[i].fields.created.split('T')[0]
        resdata['creator'] = jira_result[i].fields.creator.displayName
        try:
            resdata['assignee'] = jira_result[i].fields.assignee.displayName
        except:
            resdata['assignee'] = None
        resdata['version'] = jira_result[i].fields.versions[0].name
        resdata['status'] = jira_result[i].fields.status.name
        resdata['priority'] = jira_result[i].fields.customfield_11294[0].value
        resdata['describe'] =  jira_result[i].fields.summary
        data.append(resdata)
    return data

def ecsbymonthpageresult():
    """
    分页改造
    :param :ecsid
        :createdate
        :describe 摘要
        :creater 创建者
        :version 版本
        :status 状态
        assignee 经办人
        priority: 优先级
    :return:return ecs by this month
    """
    csechildsql = 'project in ("EasyStack Customer Support") AND createdDate  >= endOfMonth(-1)'
    jira_result = cseinfoinit.jirasql(csechildsql)
    data = []
    for i in range(len(jira_result)):
        resdata = {}
        resdata['ecsid'] = jira_result[i].key
        resdata['createdate']=jira_result[i].fields.created.split('T')[0]
        resdata['creator'] = jira_result[i].fields.creator.displayName
        resdata['assignee'] = jira_result[i].fields.assignee.displayName
        resdata['version'] = jira_result[i].fields.versions[0].name
        resdata['status'] = jira_result[i].fields.status.name
        resdata['priority'] = jira_result[i].fields.customfield_11294[0].value
        resdata['describe'] =  jira_result[i].fields.summary
        data.append(resdata)
    return data

def getcsetotals():
    tbcse = TbCse.objects.all()
    json_data = serializers.serialize('json', tbcse)
    resdata = json.loads(json_data)
    return resdata

def updatecsetotals():
    csetotalsql = 'project in (CustomerEnvironment) AND issuetype  = Epic AND status != Done '
    csetotalresult = cseinfoinit.jirasql(csetotalsql)
    resultdata = []
    for i in csetotalresult:

        try:
            tbcseid = TbCse.objects.filter(cseid=str(i.key))
            if tbcseid.first() is not None:
                continue
            else:
                data = {}
                data['cseid'] = i.key
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
                tbcse = TbCse(cseid=data['cseid'], csename=data['csename'], csestatus=data['csestatus'],
                              customername=data['customername'],
                              projectname=data['projectname'], fullname=data['fullname'],
                              version=data['version'], maintenancedate=data['maintenancedate'],
                              environmenttype=data['environmenttype'])
                tbcse.save()
        except:
            data = {}
            data['cseid'] = i.key
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
            tbcse = TbCse(cseid=data['cseid'], csename=data['csename'], csestatus=data['csestatus'],
                          customername=data['customername'],
                          projectname=data['projectname'], fullname=data['fullname'],
                          version=data['version'], maintenancedate=data['maintenancedate'],
                          environmenttype=data['environmenttype'])
            tbcse.save()
    result = 'ok'
    return result


def selectcse(cseid='', csename='', customername=''):

    if cseid:
        cseinfo = TbCse.objects.filter(cseid__icontains=cseid)
        json_data = serializers.serialize('json', cseinfo)

        resdata = json.loads(json_data)
        return resdata
    elif csename:
        cseinfo = TbCse.objects.filter(csename__icontains=csename)
        json_data = serializers.serialize('json', cseinfo)
        print(json.loads(json_data))
        resdata = json.loads(json_data)
        return resdata
    elif customername:
        cseinfo = TbCse.objects.filter(customername__icontains=customername)
        json_data = serializers.serialize('json', cseinfo)
        print(json.loads(json_data))
        resdata = json.loads(json_data)
        return resdata




def csemonth(csekey):
    data = csechildresult(csekey)
    reyear=str(datetime.date.today().year)
    rdata=[0]*12
    # rdata = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0}
    for i in data:
        #这个循环有点纯 需要优化
        #前端数据获取返回字典会乱，改成返回列表 ？
        if reyear+'-01-' in i['createdata']:
            # rdata['01']+=1
            rdata[0] += 1
        elif reyear+'-02-' in i['createdata']:
            # rdata['02']+=1
            rdata[1] += 1
        elif reyear+'-03-' in i['createdata']:
            # rdata['03']+=1
            rdata[2] += 1
        elif reyear+'-04-' in i['createdata']:
            # rdata['04']+=1
            rdata[3] += 1
        elif reyear+'-05-' in i['createdata']:
            # rdata['05']+=1
            rdata[4] += 1
        elif reyear+'-06-' in i['createdata']:
            # rdata['06']+=1
            rdata[5] += 1
        elif reyear+'-07-' in i['createdata']:
            # rdata['07']+=1
            rdata[6] += 1
        elif reyear+'-08-' in i['createdata']:
            # rdata['08']+=1
            rdata[7] += 1
        elif reyear+'-09-' in i['createdata']:
            # rdata['09']+=1
            rdata[8] += 1
        elif reyear+'-10-' in i['createdata']:
            # rdata['10']+=1
            rdata[9] += 1
        elif reyear+'-11-' in i['createdata']:
            # rdata['11']+=1
            rdata[10] += 1
        elif reyear+'-12-' in i['createdata']:
            # rdata['12']+=1
            rdata[11] += 1

    return rdata


class GetCsetotalView(APIView):
    def get(self, equest):
        '''列表视图：查询基础信息'''

        csetotal = getcsetotals()

        return Response(csetotal)

class UpdateCsetotalView(APIView):
    def get(self, equest):
        '''列表视图：查询基础信息'''

        csetotal = updatecsetotals()
        return Response(csetotal)

class CseDescribeView(APIView):
    def get(self,request):
        '''列表视图：查询基础信息'''
        pks= request.query_params.get('csekey')
        cseinfo = cseresult(pks)
        return Response(cseinfo)


class EsdeskView(APIView):
    def get(self,request):
        '''列表视图：查询基础信息'''
        esdeskid = request.query_params.get('esdeskid')
        esdeskinfo = esdeskresult(esdeskid)
        return Response(esdeskinfo)

class CseTypeView(APIView):
    def get(self, request):
        csekey = request.query_params.get('csekey')
        data = csetyperesult(csekey)
        return Response(data)
    def put(self,request):
        return Response()
class CseChildView(APIView):
    def get(self, request):
        csekey = request.query_params.get('csekey')
        data = csechildresult(csekey)
        return Response(data)
    def put(self,request):
        return Response()
class CseMonthView(APIView):

    def get(self, request):
        '''
        :param request:
        :return: 当年这个项目每月case量
        '''
        csekey = request.query_params.get('csekey')
        data = csemonth(csekey)
        return Response(data)
    def put(self,request):
        return Response()


class UserCaseView(APIView):
    def get(self, request):
        userid = request.query_params.get('userid')
        data = usercaseresult(userid)
        return Response(data)

class SelectCseView(APIView):
    def get(self, request):
        cseid = request.query_params.get('cseid')
        csename = request.query_params.get('csename')
        customername= request.query_params.get('customername')
        data = selectcse(cseid, csename, customername)
        return Response(data)
    def post(self,request):
        cseid = request.data.get('cseid')
        csename = request.data.get('csename')
        customername = request.data.get('customername')
        data = selectcse(cseid, csename, customername)
        return Response(data)

class EcsByMonthView(APIView):
    def get(self, request):
        # userid = request.query_params.get('userid')
        data = ecsbymonthresult()
        return Response(data)

class EcsByMonthPageView(APIView):
    """
    分页改造
    """
    def get(self, request):
        # 从路由当中获取当前页的页码和每页显示数量
        current_page = request.query_params.get('currentPage',1)
        page_size = request.query_params.get('pageSize',3)
        #获取所有数据
        data = ecsbymonthresult()
        # 实例化分页器
        paginotor = Paginator(data, page_size)
        # 获取当前页的数据
        pagdata = paginotor.page(current_page)
        # 序列化
        # data_serializer = serializers.serialize('json',pagdata)
        resdata = {
            'data': list(pagdata),  # 当前的数据
            # 'data': data_serializer.data,  # 当前的数据
            'page_list': [i for i in paginotor.page_range],  # 分页的页码列表
            'page_sum': paginotor.num_pages,  # 总页数
            # 'total': data.count()  # 总共有多少条内容
            'total': len(data)  # 总共有多少条内容
        }
        return Response(resdata)

from .tempofilltime import FillTime

class FilltempoView(APIView):
    def get(self, request):
        userid = request.query_params.get('userid')
        # print(userid)
        data = usercaseresult(userid)
        return Response(data)
    def post(self,request):
        ss = request.data
        workerId = request.data.get('workerId'),
        #用户id
        esdeskid = request.data.get('esdeskid'),
        Authorization = request.data.get('Authorization'),
        #将填写得工时时间
        tompetime = request.data.get('tompetime'),
        #是否自动填写工时
        filldatetime = request.data.get('filldatetime')
        is_autofill = request.data.get('is_autofill'),
        result = FillTime(Authorization[0], tompetime[0], esdeskid, workerId[0], filldatetime, is_autofill[0])
        return Response(result)

class JiraUserloginView(APIView):
    def get(self, request):
        jiraid = request.query_params.get('jiraid')
        data = userresult(jiraid)
        return JsonResponse(data, safe=False)
    def post(self, request):
        jiraname = request.data.get('jiraemail')
        jirakey = request.data.get('jirakey')
        data = jirausrresult(jiraname, jirakey)
        return JsonResponse(data, safe=False)

class TotpView(APIView):
    def get(self, request):
        csekey = request.query_params.get('csekey')
        data = csechildresult(csekey)
        return Response(data)
    def post(self,request):

        jiraemail = request.data.get('jiraemail')
        totp_type = request.data.get('totp_type')
        totp_version = request.data.get('totp_version')
        Dynamicpwd = request.data.get('Dynamicpwd')
        datas = request.data.get('datas')
        data = totpresult(jiraemail,Dynamicpwd,datas,totp_type,totp_version)
        return Response(data)
