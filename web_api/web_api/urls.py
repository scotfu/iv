from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#import records.urls
from django.conf import settings
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/',include(admin.site.urls)),
    url(r'^', include('records.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
)

urlpatterns += patterns('',
                        url(r'^static/(?P<path>.*)$',
                            'django.views.static.serve',
                            {'document_root': settings.STATIC_ROOT, },
                            name='static'),
)