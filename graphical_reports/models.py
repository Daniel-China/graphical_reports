#!/usr/bin/env python
#encoding:utf8
from  django.db import models



class table_info(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_theme = models.CharField(max_length=40)
    t_title = models.CharField(max_length=100)
    t_type = models.CharField(max_length=40)
    t_iscofig = models.BooleanField()