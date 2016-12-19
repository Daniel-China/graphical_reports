#!/usr/bin/env python
#encoding:utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    table_data = []
    return render_to_response('chartManage.html', locals())


@csrf_exempt
def GetChartType(request):
    char_type = [{'display' : "折线图", 'value' : "line"}, {'display' : "柱状图", 'value' : "bar"}]
    # char_type = ["line","bar"]
    print json.dumps(char_type)
    return HttpResponse(json.dumps(char_type), content_type="application/json")