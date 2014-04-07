#! /usr/bin/env python
#coding=utf-8
from django.conf.urls import patterns, url
from .views import record, bitstring, record_search, bit_string_search


urlpatterns = patterns('',
    url(r'^record/(?P<record_id>\d+)/$', record, name='record'),
    url(r'^bitstring/(?P<b_id>\d+)/$', bitstring,name='bit_string'),
    url(r'^record/search/$', record_search,name='record_search'),
    url(r'^bitstring/search/$', bit_string_search,name='bit_string_search'),
    )
