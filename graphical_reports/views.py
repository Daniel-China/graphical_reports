#!/usr/bin/env python
#encoding:utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse

def home(request):
    table_data = []
    return render_to_response('base.html', locals())