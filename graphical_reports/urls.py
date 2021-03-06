from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'graphical_reports.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'graphical_reports.views.home', name='home'),
    url(r'^chartShow', 'graphical_reports.views.chart_show'),
    url(r'^getcsv$', 'graphical_reports.views.get_CSV'),
    url(r'^list$', 'graphical_reports.views.chart_dir'),
    url(r'^getNewChartOption$', 'graphical_reports.views.get_NewChartOption'),
    url(r'^getEditOption$', 'graphical_reports.views.get_EditOption'),
    url(r'^getDelOption$', 'graphical_reports.views.get_DelOption'),
    url(r'^getExtOption$', 'graphical_reports.views.get_ExtOption'),
    url(r'^getsource$', 'graphical_reports.views.get_Source'),
    url(r'^EditChart$', 'graphical_reports.views.edit_chart'),
    url(r'^extEditChart$', 'graphical_reports.views.ext_edit_chart'),
    url(r'^addNewChart$', 'graphical_reports.views.add_NewChart'),
    url(r'^delChart$', 'graphical_reports.views.del_chart'),
    url(r'^runSql$', 'graphical_reports.views.runSql'),
    url(r'^saveChart$', 'graphical_reports.views.save_Chart'),
    url(r'^saveJson$', 'graphical_reports.views.save_Json'),
    url(r'^uploadCSV$', 'graphical_reports.views.upload_CSV'),
    url(r'^api$', 'graphical_reports.views.offline_api'),
    url(r'^doc$', 'graphical_reports.views.offline_doc'),
    url(r'^map$', 'graphical_reports.views.map_test'),
)
