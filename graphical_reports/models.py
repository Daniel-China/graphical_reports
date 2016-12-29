#!/usr/bin/env python
#encoding:utf8
from  django.db import models



class ChartInfo(models.Model):
    '''图表所有配置信息'''
    id = models.AutoField(primary_key=True)
    theme = models.CharField(max_length=40)
    name = models.CharField(max_length=100, unique=True, )
    type = models.CharField(max_length=40)
    is_config = models.BooleanField()
    group_name = models.ForeignKey('ChartGroup')
    sql_exec = models.TextField()
    sql_desc = models.TextField()
    sql_data = models.TextField()
    excel_data = models.TextField()
    bonding_info = models.TextField()


    title_config = models.TextField()
    legend_config = models.TextField()
    grid_config = models.TextField()
    xAxis_config = models.TextField()
    yAxis_config = models.TextField()
    dataZoom_config = models.TextField()
    tooltip_config = models.TextField()
    toolbox_config = models.TextField()
    series_config = models.TextField()
    preview_config = models.TextField()

class ChartGroup(models.Model):
    '''图表分组信息'''
    group_name = models.CharField(max_length=40)
    display_flag = models.CharField(max_length=10)
    order_num = models.CharField(max_length=20)


class ConfigOption(models.Model):
    '''配置项可选项'''

    theme_default = models.TextField()
    theme_option = models.TextField()

    title_default = models.TextField()
    title_show = models.TextField()
    title_textAlign = models.TextField()
    title_Baseline = models.TextField()

    legend_default = models.TextField()
    legend_show = models.TextField()

    grid_default = models.TextField()
    grid_show = models.TextField()

    xAxis_default = models.TextField()
    xAxis_type = models.TextField()
    yAxis_default = models.TextField()
    yAxis_type = models.TextField()

    dataZoom_default = models.TextField()
    dataZoom_show = models.TextField()
    dataZoom_type = models.TextField()

    tooltip_default = models.TextField()
    tooltip_trigger = models.TextField()

    toolbox_default = models.TextField()
    toolbox_show = models.TextField()
    toolbox_feature_saveAsimage = models.TextField()
    toolbox_feature_show = models.TextField()
    toolbox_feature_type = models.TextField()
    toolbox_restore_show = models.TextField()
    toolbox_dataView_show = models.TextField()

    series_default = models.TextField()
    series_type = models.TextField()
