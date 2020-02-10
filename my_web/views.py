# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render, render_to_response
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
from models import *
from django.contrib.auth import authenticate
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
import datetime
import smtplib
import time
import re


@csrf_exempt
def getoptionalfund(request):
    myresponse = {}
    fundInformations = json.loads(
        serializers.serialize("json", optionalfund.objects.all()))
    fundlist = []
    yesterday = datetime.datetime.now().strftime('%Y-%m-%d')
    for fundInformation in fundInformations:
        fundcode = fundInformation['fields']['fundcode']
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
        buy = float(information['gszzl'])
        if buy < 0:
            buy = 1000*round(abs(buy))
            information['buy'] = buy
        information['hold'] = fundInformation['fields']['hold']
        information['progressiveincome'] = fundInformation['fields']['progressiveincome']
        information['rateofreturn'] = fundInformation['fields']['rateofreturn']
        information['gszzl'] = information['gszzl']+'%'
        information['budgetrevenue'] = float(
            information['hold'])*float(information['gszzl'].replace("%", ''))/100
        # print yesterday
        if yesterday == information['date']:
            information['earningstoday'] = float(
                information['hold'])*float(information['networth'].replace("%", ''))/100
        fundlist.append(information)
    myresponse['list'] = fundlist
    return JsonResponse(myresponse)

@csrf_exempt
def getmarket(request):
    myresponse = {}
    informationlist=[]
    marketlist = ['s_sh000001','s_sz399006']
    for market in marketlist:
        print market
        stock={}
        url = 'https://hq.sinajs.cn/list={0}'.format(
            market)
        information = re.search(r'\"(.+?)\"',
                       requests.get(url=url).text, re.M | re.I)
        informations =information.group(1).split(",")
        stock['name']=informations[0]
        stock['stockcode']=market
        stock['latestprice']=informations[1]
        stock['quotechange']=informations[3]+'%'
        informationlist.append(stock)
    myresponse['stock'] = informationlist
    return JsonResponse(myresponse)

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
    except:
        myresponse['message'] = "您输入的基金代码错误！！！"
    return JsonResponse(myresponse)
