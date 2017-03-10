#!/usr/bin/env python
# encoding:utf8
from django.shortcuts import render_to_response, render
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from models import ChartGroup, ChartInfo, ConfigOption, DataSource
from datetime import date, datetime, timedelta
import json, MySQLdb, pymysql, csv


class CJsonEncoder(json.JSONEncoder):
    """Json的子类，用于转换date或者datetime类型的数据"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, timedelta):
            return (datetime(2017, 2, 3, 00, 00, 00) + obj).strftime('%H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


def home(request):
    table_data = []
    # print new_table_create(request)
    return render_to_response('chartManage.html', locals())

def offline_api(request):
    return render_to_response('echarts-doc-offline/api.html', locals())

def offline_doc(request):
    return render_to_response('echarts-doc-offline/option.html', locals())


@never_cache
@csrf_exempt
def get_NewChartOption(request):
    default_option = ConfigOption.objects.get(id=1)
    group_name = []
    for i in ChartGroup.objects.all():
        group_name.append(i.group_name)
    new_table_option = {'chart_type': json.loads(default_option.series_type),
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
def get_DelOption(request):
    chart_name = []
    for i in ChartInfo.objects.all():
        chart_name.append(i.name)
    edit_option = {'chart_name': chart_name}
    return HttpResponse(json.dumps(edit_option), content_type="application/json")


@csrf_exempt
def get_ExtOption(request):
    chart_name = []
    for i in ChartInfo.objects.all():
        chart_name.append(i.name)
    edit_option = {'chart_name': chart_name}
    return HttpResponse(json.dumps(edit_option), content_type="application/json")



@csrf_exempt
def get_Source(request):
    if request.method == 'POST':
        source_name = request.body
        if source_name == '':
            source_config = {'host': '', 'port': '', 'db_name': '', 'user': '', 'passwd': ''}
        else:
            source = DataSource.objects.get(source_name=request.body)
            source_config = {'host': source.host,
                             'port': source.port,
                             'db_name': source.db_name,
                             'user': source.user_name,
                             'passwd': source.passwd}
    return HttpResponse(json.dumps(source_config), content_type="application/json")



@csrf_exempt
def add_NewChart(request):
    # if request.is_ajax() and request.method == 'POST':
    # print request.POST["newTableName"]
    new_table_name = request.GET.get('newTableName')
    print request.GET['newTableName']
    print new_table_create(request)
    return HttpResponse(json.dumps(new_table_name), content_type="application/json")


@csrf_exempt
def del_chart(request):
    """删除图表"""
    req = json.loads(request.body)
    req_post = {}
    for i in req:
        req_post[i["name"]] = i["value"]
    table_name = req_post['delTableName']
    res = []
    if table_name == req_post['confirmTableName']:
        try:
            ChartInfo.objects.filter(name=table_name).delete()
            res = "删除"
        except Exception, err:
            print err
    else:
        res = "删除不"

    return HttpResponse(json.dumps(res), content_type="application/json")


@csrf_exempt
def ext_edit_chart(request):
    '''高级图表配置'''
    if request.method == 'POST':
        table_name = request.POST.get("extTableName")
        chart_json = ChartInfo.objects.get(name=table_name)
        chart_pre = chart_json.preview_config

    return render_to_response('ace.html', locals())


def new_table_create(request):
    """生成新图表基本配置"""
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
                              type=request.GET.get("newTableType"),
                              dataZoom_config=request.GET.get("zoomNum"),
                              is_config=False,
                              group_name=ChartGroup.objects.get(group_name=request.GET.get("newTableGroup")),
                              preview_config=json.dumps(new_table_config))
        new_table.save()
    except Exception, err:
        print err
    return new_table_config


@csrf_exempt
def edit_chart(request):
    '''图表编辑页面'''
    if request.method == 'POST':
        chart_name = request.POST.get("TableName")
        source_type = request.POST.get("DataSource")
        target_obj = ChartInfo.objects.get(name=chart_name)
        target_obj.source_type = source_type
        target_obj.save()
        if source_type == 'csv':
            target_page = 'csv_import.html'


        else:
            target_page = 'chartEdit.html'
        data_source = DataSource.objects.all()
        data_source_name = []
        for i in data_source:
            data_source_name.append(i.source_name)


    return render_to_response(target_page, locals())


@csrf_exempt
def runSql(request):
    """数据源配置"""
    if request.method == 'POST':

        try:
            req = json.loads(request.body)
            req_post = {}
            for i in req:
                req_post[i["name"]] = i["value"]
            db_sql = req_post["dbSql"]
            conn = pymysql.connect(host=req_post["host"],
                                   user=req_post["user"],
                                   passwd=req_post["password"],
                                   db=req_post["dbName"],
                                   port=int(req_post["port"]),
                                   charset='utf8')
            cur = conn.cursor()
            cur.execute(db_sql)
            desc = [d[0] for d in cur.description]
            xyaxis = [['x', 'x轴-刻度'], ['y', 'y轴-图例']]
            print desc
            insert_txt = render_to_response("bondingTable.html", locals()).content
            new_table = ChartInfo.objects.get(name=req_post["chartName"])
            new_table.sql_exec = json.dumps(req_post)
            new_table.sql_desc = json.dumps(desc)
            # new_table.sql_data = json.dumps(dict(zip(desc, zip(*cur.fetchall()))), cls=CJsonEncoder)
            new_table.save()
            """保存查询结果的字段和数据"""

            cur.close()
            conn.close()
        except Exception, err:
            print err

    else:
        pass

    return HttpResponse(json.dumps(insert_txt), content_type="application/json")


@csrf_exempt
def upload_CSV(request):
    """csv上传导入"""
    if request.method == 'POST':
        req = request.FILES
        field_name = ''
        destination_path = ''
        try:
            for field_name in req:
                uploaded_file = request.FILES[field_name]
                print uploaded_file.name
                destination_path = './csv/%s.csv' % (field_name)
                destination = open(destination_path, 'wb+')
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
                destination.close()

        except Exception, err:
            print err
        with open(destination_path, 'rb') as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
            desc = rows[0]
            xyaxis = [['x', 'x轴-刻度(分类)'], ['y', 'y轴-图例(数据)']]
            insert_txt = render_to_response("bondingTable.html", locals()).content
            new_table = ChartInfo.objects.get(name=field_name)

            new_table.sql_desc = json.dumps(desc)
            print insert_txt

        return HttpResponse(insert_txt, content_type="application/json")
    else:
                # show the upload UI
        return HttpResponse('错误', content_type="application/json")




@csrf_exempt
def save_Chart(request):
    """保存绑定信息"""
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            req_post = {}
            for i in req:
                req_post[i["name"]] = i["value"]
            new_table = ChartInfo.objects.get(name=req_post["chartName"])
            new_table.bonding_info = json.dumps(req_post)
            new_table.is_config = True
            new_table.save()

        except Exception, err:
            print err

    return HttpResponse(json.dumps(req_post), content_type="application/json")

@csrf_exempt
def save_Json(request):
    """保存高级配置"""
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            print json.dumps(req["json"])
            req_post = ''
            # for i in req:
            #     req_post[i["name"]] = i["value"]
            new_table = ChartInfo.objects.get(name=req["chart_name"])
            new_table.preview_config = json.dumps(req["json"])
            new_table.save()

        except Exception, err:
            print err

    return HttpResponse(json.dumps(err), content_type="application/json")


@csrf_exempt
def chart_dir(request):
    """展示页"""
    ChartInfoAll = ChartInfo.objects.all()
    groups = ChartGroup.objects.all()
    charts = []
    for Chart in ChartInfoAll:
        if Chart.is_config:
            charts.append(Chart)

    return render_to_response('chartDir.html', locals())


@csrf_exempt
def chart_show(request):
    """图表展示界页生成"""
    try:
        if request.GET.get("group"):
            pass
        elif request.GET.get("chart"):
            chart_obj = ChartInfo.objects.get(id=request.GET.get("chart"))
            theme = chart_obj.theme

            chart_json = make_chart_config(chart_obj)

    except Exception, err:
        print err

    return render(request, 'chartViews.html', locals())


def make_chart_config(chart_obj):
    """合成图表配置json"""
    chart_config = json.loads(chart_obj.preview_config)
    if chart_obj.source_type == 'mysql':
        print chart_obj.type

        # chart_data = json.loads(chart_obj.sql_data)
        chart_bonding = json.loads(chart_obj.bonding_info)
        chart_exec = json.loads(chart_obj.sql_exec)
        try:
            conn = pymysql.connect(host=chart_exec["host"],
                                   user=chart_exec["user"],
                                   passwd=chart_exec["password"],
                                   db=chart_exec["dbName"],
                                   port=int(chart_exec["port"]),
                                   charset='utf8')
            cur = conn.cursor()
            cur.execute(chart_exec["dbSql"])
            desc = [d[0] for d in cur.description]
            results_all = cur.fetchall()
            chart_data = json.loads(json.dumps(dict(zip(desc, zip(*results_all))), cls=CJsonEncoder))

        except Exception, err:
            print err
    elif chart_obj.source_type == 'csv':
        destination_path = './csv/%s.csv' % (chart_obj.name)
        with open(destination_path, 'rb') as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
            desc = rows[0]
            results_all = rows[1:]
            chart_data = json.loads(json.dumps(dict(zip(desc, zip(*results_all))), cls=CJsonEncoder))


    if chart_obj.type == 'line' or chart_obj.type == 'bar':
        try:
            legend = []
            desc = []
            for col in json.loads(chart_obj.sql_desc):
                if chart_bonding[col + '_type'] == 'y':
                    if len(chart_bonding[col + '_display']):
                        legend.append(chart_bonding[col + '_display'])
                    else:
                        legend.append(col)
                    desc.append(col)
                elif chart_bonding[col + '_type'] == 'x':
                    chart_config['xAxis'][0]['data'] = chart_data[col]
                    chart_config['xAxis'][0]['name'] = chart_bonding[col + '_display']
                    chart_config['dataZoom'][0]['endValue'] = len(chart_data[col])
                    if int(chart_obj.dataZoom_config) >= len(chart_data[col]):
                        chart_config['dataZoom'][0]['startValue'] = 0
                    else:
                        chart_config['dataZoom'][0]['startValue'] = len(chart_data[col]) - int(chart_obj.dataZoom_config)


            chart_config['legend']['data'] = legend
            pre_series = chart_config['series'][0]
            pre_series['type'] = chart_obj.type
            chart_config['series'] = [col for col in desc]
            series = []

            for i, col in enumerate(desc):
                pre = pre_series
                pre['name'] = chart_bonding[col + '_display']
                pre['stack'] = chart_bonding[col + '_display']
                pre['data'] = chart_data[col]
                # print json.dumps(pre)
                series.append(json.dumps(pre))
                # print series
            chart_config['series'] = [json.loads(col) for col in series]
        except Exception, err:
            print err

    elif chart_obj.type == 'pie':
        try:
            del chart_config['xAxis']
            del chart_config['yAxis']
            del chart_config['dataZoom']
            chart_config['legend']['data'] = zip(*results_all)[0]
            pre_series = {}
            pre_series['type'] = 'pie'
            pre_series['data'] = []
            for kv in results_all:
                option = {'name': kv[0], 'value': kv[1]}
                pre_series['data'].append(option)
            print json.dumps(pre_series, cls=CJsonEncoder)
            chart_config['series']=[json.loads(json.dumps(pre_series, cls=CJsonEncoder)),]
        except Exception, err:
            print err
    print json.dumps(chart_config, cls=CJsonEncoder )
    return json.dumps(chart_config, cls=CJsonEncoder )