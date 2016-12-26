from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'graphical_reports.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'graphical_reports.views.home', name='home'),
    url(r'^getNewChartOption$', 'graphical_reports.views.get_NewChartOption'),
    url(r'^getEditOption$', 'graphical_reports.views.get_EditOption'),
    url(r'^EditChart$', 'graphical_reports.views.edit_chart'),
    url(r'^addNewChart$', 'graphical_reports.views.add_NewChart'),
    url(r'^runSql$', 'graphical_reports.views.runSql'),
    url(r'^saveChart$', 'graphical_reports.views.save_Chart'),
)
