#!/usr/bin/env python
#encoding:utf8
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from models import ChartGroup,ChartInfo,ConfigOption
import json

def home(request):
    table_data = []
    print new_table_create()
    return render_to_response('chartManage.html', locals())

@never_cache
@csrf_exempt
def get_NewChartOption(request):
    default_option = ConfigOption.objects.get(id = 1)
    group_name = []
    for i in ChartGroup.objects.all():
        group_name.append(i.group_name)
    new_table_option ={'chart_type': json.loads(default_option.series_type),
                       'chart_group': group_name,
                       'chart_theme': json.loads(default_option.theme_option)}
    # char_type = ["line","bar"]
    print json.dumps(new_table_option)
    print ConfigOption.objects.all()

    return HttpResponse(json.dumps(new_table_option), content_type="application/json")


@csrf_exempt
def add_NewChart(request):
    # if request.is_ajax() and request.method == 'POST':
    # print request.POST["newTableName"]
    new_table_name = request.GET['newTableName']
    print request.GET['newTableName']

    return HttpResponse(json.dumps(new_table_name), content_type="application/json")


def new_table_create():
    default_option = ConfigOption.objects.get(id=1)
    new_table_config = {'title': json.loads(default_option.title_default),
                        'legend': json.loads(default_option.legend_default),
                        'xAxis': json.loads(default_option.xAxis_default),
                        'yAxis': json.loads(default_option.yAxis_default),
                        'dataZoom': json.loads(default_option.dataZoom_default),
                        'tooltip': json.loads(default_option.tooltip_default),
                        'toolbox': json.loads(default_option.toolbox_default),
                        'series': json.loads(default_option.series_default)
                        }
    return json.dumps(new_table_config)