from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'graphical_reports.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'graphical_reports.views.home', name='home'),
    url(r'^GetNewChartOption$', 'graphical_reports.views.get_NewChartOption'),
)
