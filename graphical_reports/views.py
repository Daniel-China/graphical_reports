#!/usr/bin/env python
#encoding:utf8
from django.shortcuts import render_to_response,render
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from models import ChartGroup,ChartInfo,ConfigOption
from datetime import date, datetime
import json,MySQLdb,sqlite3


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

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
    except Exception,err:
        print err
    return new_table_config


@csrf_exempt
def edit_chart(request):
    if request.method == 'POST':
        chart_name = request.POST.get("TableName")


    return render_to_response('chartEdit.html', locals())

@csrf_exempt
def runSql(request):
    '''数据源配置'''
    if request.method == 'POST':

        try:
            req = json.loads(request.body)
            req_post = {}
            for i in req:
                req_post[i["name"]] = i["value"]
            db_sql = req_post["dbSql"]
            conn = MySQLdb.Connect(req_post["host"],
                                   req_post["user"],
                                   req_post["password"],
                                   req_post["dbName"],
                                   int(req_post["port"]),
                                   charset='utf8')
            cur = conn.cursor()
            cur.execute(db_sql)
            desc = [d[0] for d in cur.description]
            xyaxis = [['x','x轴-刻度'],['y', 'y轴-图例']]
            print desc
            insert_txt = render_to_response("bondingTable.html",locals()).content
            new_table = ChartInfo.objects.get(name=req_post["chartName"])
            new_table.sql_exec = json.dumps(req_post)
            new_table.sql_desc = json.dumps(desc)
            new_table.sql_data = json.dumps(dict(zip(desc, zip(*cur.fetchall()))), cls=CJsonEncoder)
            new_table.save()
            cur.close()
            conn.close()
        except Exception,err:
            print err

    else:
        pass

    return HttpResponse(json.dumps(insert_txt), content_type="application/json")



@csrf_exempt
def save_Chart(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            req_post = {}
            for i in req:
                req_post[i["name"]]=i["value"]
            new_table = ChartInfo.objects.get(name=req_post["chartName"])
            new_table.bonding_info = json.dumps(req_post)
            new_table.is_config = True
            new_table.save()

        except Exception,err:
            print err

    return HttpResponse(json.dumps(req_post), content_type="application/json")


@csrf_exempt
def chart_dir(request):
    '''展示页'''
    ChartInfoAll = ChartInfo.objects.all()
    groups = ChartGroup.objects.all()
    charts = []
    for Chart in ChartInfoAll:
        if Chart.is_config:
            charts.append(Chart)

    return render_to_response('chartDir.html', locals())


@csrf_exempt
def chart_show(request):
    try:
        if request.GET.get("group"):
            pass
        elif request.GET.get("chart"):
            chart_obj = ChartInfo.objects.get(id=request.GET.get("chart"))
            theme = chart_obj.theme
            chart_json = make_chart_config(chart_obj)
    except Exception, err:
        print err

    return render(request,'chartViews.html', locals())

def make_chart_config(chart_obj):
    '''合成图表配置json'''
    chart_config = json.loads(chart_obj.preview_config)
    chart_data = json.loads(chart_obj.sql_data)
    chart_bonding = json.loads(chart_obj.bonding_info)
    legend = []
    desc = []
    try:
        for col in json.loads(chart_obj.sql_desc):
            if chart_bonding[col+'_type'] == 'y':
                if len(chart_bonding[col+'_display']):
                    legend.append(chart_bonding[col + '_display'])
                else:
                    legend.append(col)
                desc.append(col)
            elif chart_bonding[col+'_type'] == 'x':
                chart_config['xAxis'][0]['data'] = chart_data[col]

        chart_config['legend']['data'] = legend
        pre_series = chart_config['series'][0]
        chart_config['series'] = []

        for i,col in enumerate(legend):
            pre_series['name'] = col
            pre_series['stack'] = col
            pre_series['data'] = chart_data[desc[i]]
            chart_config['series'].append(pre_series)
        print chart_config
    except Exception, err:
        print err

    return json.dumps(chart_config)