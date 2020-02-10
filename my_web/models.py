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