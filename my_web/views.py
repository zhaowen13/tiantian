# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
from .models import *
from django.contrib.auth import authenticate
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
import datetime
import smtplib
import time
import re
from dwebsocket.decorators import accept_websocket
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

income_list ={}

# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用默认的DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), 'default')

# @register_job(scheduler, 'cron', id='income', hour=9, minute=15)
# def income_job():
#     print("定时任务啊")
#     for income in income_list:
#         # hold =hold=income['earningstoday']
#         hold=optionalfund.objects.filter(fundcode=income['fundcode']).values('hold')
#         hold=float(hold[0]['hold'])
#         hold =hold+float(income['budgetrevenue'])
#         optionalfund.objects.filter(fundcode=income['fundcode']).update(
#         hold=hold,
#     )
# register_events(scheduler)
# scheduler.start()

@accept_websocket
@csrf_exempt
def getoptionalfund(request):  #基金
    if request.is_websocket():
        myresponse = []
        while 1:
            fundInformations = json.loads(
                serializers.serialize("json", optionalfund.objects.all()))
            fundlist = []
            if not (datetime.datetime.now().hour >23 and  myresponse):
                # print(datetime.datetime.now().hour)
                yesterday = datetime.datetime.now().strftime('%Y-%m-%d')
                for fundInformation in fundInformations:
                    fundcode = fundInformation['fields']['fundcode']
                    name = fundInformation['fields']['name']
                    # latestprice=0
                    url = 'http://fundgz.1234567.com.cn/js/{0}.js'.format(
                        fundcode)
                    information = json.loads(requests.get(
                        url=url).text.replace("jsonpgz(", '').replace(");", ''))
                    url2 = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&page=1&per=1'.format(
                        fundcode)
                    jz = re.search(r'grn\'>(.+?)%',
                                requests.get(url=url2).text, re.M | re.I)
                    if jz == None:
                        jz = re.search(r'red\'>(.+?)%',
                                    requests.get(url=url2).text, re.M | re.I)
                    information['networth'] = jz.group(1)+'%'
                    date = re.search(r'<tr><td>(.+?)</td>',
                                    requests.get(url=url2).text, re.M | re.I)
                    information['date'] = date.group(1)
                    gszzl = float(information['gszzl'])
                    # information['gszzl']=information['gszzl']+"%"
                    trading = tradingrules.objects.filter(name=name).values()
                    trackingindex=trading[0]['trackingindex']
                    start = int(trading[0]['start'])
                    startingamount = trading[0]['startingamount']
                    secondamount = trading[0]['secondamount']
                    sellpoint = trading[0]['sellpoint']
                    sellshare = trading[0]['sellshare']
                    # for marke in marketlist['data']:
                    #     if trackingindex==marke['name']:
                    #         latestprice=int(marke['value'].split('.')[0])
                    # print "latestprice:{0}".format(latestprice)
                    # print "start:{0}".format(start)
                    # if start > latestprice:                 #当前点位小于你设置的买入点时
                    #     if gszzl < 0:
                    #         information['buy'] = 1000*round(abs(gszzl))
                    information['buy']=0
                    information['hold'] = fundInformation['fields']['hold']
                    information['hold'] = round(float(information['hold']), 2)
                    information['progressiveincome'] = fundInformation['fields']['progressiveincome']
                    information['rateofreturn'] = fundInformation['fields']['rateofreturn']
                    information['quote_change'] = information['gszzl']+'%'
                    information['budgetrevenue'] = float(
                        information['hold'])*float(information['gszzl'].replace("%", ''))/100
                    information['budgetrevenue'] = round(information['budgetrevenue'], 2)
                    if yesterday == information['date']:
                        information['earningstoday'] = float(
                            information['hold'])*float(information['networth'].replace("%", ''))/100
                        information['earningstoday'] = round(float(information['earningstoday']), 2)
                    fundlist.append(information)
                myresponse = fundlist

            request.websocket.send(json.dumps(myresponse))
            global income_list
            income_list=myresponse
            time.sleep(3) ## 向前端发送时间
    return JsonResponse({"mas":"请用长连接"})


@csrf_exempt
def buyin(request):
    myresponse = {}
    body = json.loads(request.body)
    tableData = body['form']
    myresponse['worknm'] = worknm
    return JsonResponse(myresponse)

@accept_websocket
def test_websocket(request):
    if request.is_websocket():
        while 1:
            time.sleep(3) ## 向前端发送时间
            dit = {
                'time':time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
            }
            request.websocket.send(json.dumps(dit))
    return JsonResponse({"mas":"请用长连接"})

@csrf_exempt
def holdcalculation(request):
    myresponse = {}
    yesterday = datetime.datetime.now().strftime('%Y%m%d')
    url = 'http://api.k780.com/?app=life.workday&date={0}&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json'.format(
        yesterday)
    worknm = requests.get(url=url).json()['result']['worknm']
    if worknm == u"工作日":
        hold = optionalfund.objects.all().values('hold')
        hold = hold[0]['hold']
        # hold=hold+
    myresponse['worknm'] = worknm
    return JsonResponse(myresponse)


@csrf_exempt
def addtradingrules(request):
    myresponse = {}
    body = json.loads(request.body)
    trackingindex = body['form']['trackingindex']
    start = body['form']['start']
    startingamount = body['form']['startingamount']
    secondamount = body['form']['secondamount']
    sellpoint = body['form']['sellpoint']
    sellshare = body['form']['sellshare']
    name = body['name']
    tradingrules.objects.filter(name=name).update(
        trackingindex=trackingindex,
        start=start,
        startingamount=startingamount,
        secondamount=secondamount,
        sellpoint=sellpoint,
        sellshare=sellshare,
    )
    myresponse['message'] = "添加成功"
    return JsonResponse(myresponse)

@csrf_exempt
def gettradingrules(request):
    myresponse = {}
    name = request.GET['name']
    tradin=tradingrules.objects.filter(name=name).values()
    myresponse['data'] = tradin[0]
    return JsonResponse(myresponse)

@accept_websocket
@csrf_exempt
def getmarket(request):   #股票
    data = serializers.serialize("json", stock.objects.all())
    data=json.loads(data)
    y=len(data)
    stock_value=[]
    for d in data:
        stock_value.append(d['fields'])
    if request.is_websocket():
        while 1:
            for i in range(0,y):
                stock_value[i]
                url = 'https://hq.sinajs.cn/list={0}'.format(
                    stock_value[i]['code'])
                information = re.search(r'\"(.+?)\"',
                                        requests.get(url=url).text, re.M | re.I)
                informations = information.group(1).split(",")
                stock_value[i]['newest'] = informations[1]
                stock_value[i]['quote_change'] = informations[3]+'%'
            request.websocket.send(json.dumps(stock_value))
            time.sleep(3) ## 向前端发送时间
    return JsonResponse({"mas":"请用长连接"})
    

@csrf_exempt
def addfund(request):
    myresponse = {}
    body = json.loads(request.body)
    add_fundcode = body['add_fundcode']
    try:
        fundcodes = optionalfund.objects.all().values('fundcode')
        fundcodelist = []
        for fundcode in fundcodes:
            fundcodelist.append(fundcode['fundcode'])
        if add_fundcode in fundcodelist:
            myresponse['message'] = "您输入的基金代码已经存在！！！"
        else:
            url = 'http://fundgz.1234567.com.cn/js/{0}.js'.format(add_fundcode)
            information = json.loads(requests.get(
                url=url).text.replace("jsonpgz(", '').replace(");", ''))
            myresponse['message'] = information['name']
            optionalfund.objects.create(
                name=information['name'],
                fundcode=add_fundcode,
                hold=0,
                progressiveincome=0,
                rateofreturn=0,
            )
            tradingrules.objects.create(
                trackingindex=u"上证指数",
                start=2900,
                startingamount=1000,
                secondamount=2800,
                sellpoint=3000,
                sellshare=50,
                name=information['name'],
            )
    except:
        myresponse['message'] = "您输入的基金代码错误！！！"
    return JsonResponse(myresponse)


