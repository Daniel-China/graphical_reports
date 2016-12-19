#!/usr/bin/env python
#encoding:utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import ChartGroup,ChartInfo,ConfigOption
import json

def home(request):
    table_data = []
    return render_to_response('chartManage.html', locals())


@csrf_exempt
def get_NewChartOption(request):
    default_option = ConfigOption.objects.get(id = 1)
    new_table_option ={'chart_type' : json.loads(default_option.series_type),
                       'chart_group' : ["FFF","EFREF","SEFWER"],
                       'chart_theme' : json.loads(default_option.theme_option)}
    # char_type = ["line","bar"]
    print json.dumps(new_table_option)
    return HttpResponse(json.dumps(new_table_option), content_type="application/json")