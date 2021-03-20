# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.


class optionalfund(models.Model):
    name = models.CharField('基金名称',max_length=100)
    fundcode = models.CharField('基金代码',max_length=100)
    hold = models.CharField('当前持有',max_length=100)
    progressiveincome = models.CharField('累计收益',max_length=100)
    rateofreturn = models.CharField('累计收益率',max_length=100)
    def __unicode__(self):
        return self.fundcode
    class Meta:
        db_table = "optionalfund"

class tradingrules(models.Model):
    trackingindex = models.CharField('跟踪指数',max_length=100)
    start = models.CharField('开始买入点数',max_length=100)
    startingamount = models.CharField('开始买入金额',max_length=100)
    secondamount = models.CharField('第二个档位买入点位',max_length=100)
    sellpoint = models.CharField('卖出点位',max_length=100)
    sellshare = models.CharField('卖出份额百分比',max_length=100)
    name = models.CharField('基金名称',max_length=100)
    def __unicode__(self):
        return self.fundcode
    class Meta:
        db_table = "tradingrules"

class stock(models.Model):
    name = models.CharField('股票名称',max_length=20)
    code = models.CharField('股票代码',max_length=20)
    newest = models.CharField('最新价',max_length=20)
    quote_change=models.CharField('涨跌幅',max_length=10)
    def __unicode__(self):
        return self.fundcode
    class Meta:
        db_table = "stock"