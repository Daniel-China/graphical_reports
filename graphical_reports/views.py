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
    # print new_table_create(request)
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

    return HttpResponse(json.dumps(new_table_option), content_type="application/json")


@csrf_exempt
def get_EditOption(request):
    chart_name = []
    for i in ChartInfo.objects.all():
        chart_name.append(i.name)
    edit_option = {'chart_name': chart_name}
    return HttpResponse(json.dumps(edit_option), content_type="application/json")


@csrf_exempt
def add_NewChart(request):
    # if request.is_ajax() and request.method == 'POST':
    # print request.POST["newTableName"]
    new_table_name = request.GET.get('newTableName')
    print request.GET['newTableName']
    print new_table_create(request)
    return HttpResponse(json.dumps(new_table_name), content_type="application/json")


def new_table_create(request):
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
    try:
        new_table_config["title"]["text"] = request.GET.get("newTableName")
        new_table = ChartInfo(name=request.GET.get("newTableName"),
                              theme=request.GET.get("newTableTheme"),
                              is_config=False,
                              group_name=ChartGroup.objects.get(group_name=request.GET.get("newTableGroup")),
                              preview_config=json.dumps(new_table_config))
        new_table.save()
    except Exception,e:
        print e
    return new_table_config


@csrf_exempt
def edit_chart(request):
    if request.method == 'POST':
        chart_name = request.POST.get("TableName")


    return render_to_response('chartEdit.html', locals())

