#!/usr/bin/env python
#coding=utf-8
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Count

from .models import Record,BitString


def record_search(request):
    if request.method =='GET':
        start_age = request.GET.get('start',1)
        end_age = request.GET.get('end',120)
        gender = request.GET.get('gender')
        page = request.GET.get('p',1)
        kwargs = {}
        if gender == 'Male':
            gender = '1'
        elif gender == 'Female':
            gender = '2'
        if gender:
            kwargs['gender'] = gender
        country = request.GET.getlist('country')
        education = request.GET.get('education')
        if education:
            kwargs['education'] = education
        if country:
            kwargs['country__in'] = country

    result = Record.objects.filter(age__range=(start_age,end_age),**kwargs)
    objects  = Paginator(result,100)
    response_data = {}
    response_data['result'] = 'success'
    response_data['p_num'] = objects.num_pages
    response_data['p'] = page
    response_data['data'] = {}
    response_data['data']['records'] = []
    try :
        object_list = objects.page(page)
    except:
        response_data['p'] = 1
        object_list = records.page(1)
    for r in object_list:
         response_data['data']['records'].append({'age': r.age, 'gender': r.get_gender_display(),
                             'country': {'id': r.country, 'name': r.get_country_display() },
                             'education': {'level': r.education, 'name': r.get_education_display()},
                             'bitstring': {'value': r.bit_string.bit_string,
                                           'url': reverse('bit_string',
                                                          kwargs={'b_id': r.bit_string.bit_string})
                                           },
                                       })
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def record_search_aggregation(request):
    if request.method =='GET':
        start_age = request.GET.get('start',1)
        end_age = request.GET.get('end',120)
        gender = request.GET.get('gender')
        page = request.GET.get('p',1)
        kwargs = {}
        if gender == 'Male':
            gender = '1'
        elif gender == 'Female':
            gender = '2'
        if gender:
            kwargs['record__gender'] = gender
        country = request.GET.getlist('country')
        education = request.GET.get('education')
        if education:
            kwargs['record__education'] = education
        if country:
            kwargs['record__country__in'] = country

    result = BitString.objects.filter(record__age__range=(start_age,end_age),**kwargs).annotate(num=Count('record'))
    objects  = Paginator(result,1000)
    response_data = {}
    response_data['result'] = 'success'
    response_data['p_num'] = objects.num_pages
    response_data['p'] = page
    response_data['data'] = {}
    response_data['data']['bitstrings'] = []
    try :
        object_list = objects.page(page)
    except:
        response_data['p'] = 1
        object_list = records.page(1)
    for r in object_list:
         response_data['data']['bitstrings'].append({
                             'bitstring': {'origin': r.bit_string,
                                           'pca': r.pca,
                                           'mds': r.mds,
                                           'nmds': r.nmds,
                                           },
                             'count': r.num,
                             })
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def record(request, record_id):
    r = Record.objects.get(id=record_id)
    response_data = {}
    response_data['result'] = 'success'
    response_data['data'] = {'age': r.age, 'gender': r.get_gender_display(),
                             'country': {'id': r.country, 'name': r.get_country_display() },
                             'education': {'level': r.education, 'name': r.get_education_display()},
                             'bitstring': {'value': r.bit_string.bit_string,
                                           'url': reverse('bit_string',
                                                          kwargs={'b_id': r.bit_string.bit_string})
                                           },
                             }
    return HttpResponse(json.dumps(response_data), content_type="application/json")



def bitstring(request, b_id):
    b = BitString.objects.get(bit_string=b_id)
    response_data = {}
    response_data['result'] = 'success'
    response_data['data'] = {'origin':b.bit_string, 'pca':b.pca, 'mds':b.mds, 'nmds':b.nmds}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    

def bit_string_search(request):
    pass
