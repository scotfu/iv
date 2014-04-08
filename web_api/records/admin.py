#! /usr/bin/env python
#coding=utf-8
from django.contrib import admin
from .models import Record,BitString


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id','age','gender','country','education','bit_string')

class BitStringAdmin(admin.ModelAdmin):
    list_display = ('bit_string','pca','mds','nmds')

admin.site.register(Record, RecordAdmin)
admin.site.register(BitString, BitStringAdmin)
