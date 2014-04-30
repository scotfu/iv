#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url
from .views import record, bitstring, record_search, bit_string_search,record_search_aggregation,record_search_group,test


urlpatterns = patterns('',
    url(r'^record/(?P<record_id>\d+)/$', record, name='record'),
    url(r'^bitstring/(?P<b_id>\d+)/$', bitstring,name='bit_string'),
    url(r'^record/search/$', record_search,name='record_search'),
    url(r'^record/search/aggregation/$', record_search_aggregation,name='record_search_aggregation'),
    url(r'^record/search/group/$', record_search_group,name='record_search_group'),
    url(r'^bitstring/search/$', bit_string_search,name='bit_string_search'),
    url(r'^test/$',test,name='test'),
    )
