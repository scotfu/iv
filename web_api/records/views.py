#!/usr/bin/env python
#coding=utf-8
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Count

from .models import Record,BitString


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = json.dumps(str(objects))

        return HttpResponse(data, "application/json")
    
    return decorator

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
        if gender != 0:
            kwargs['gender'] = gender
        country = request.GET.getlist('country')
        education = request.GET.get('education')
        if education != 0:
            kwargs['education'] = education
        if country != 0:
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
                                           'pca': r.bit_string.pca,
                                           'mds': r.bit_string.mds,
                                           'nmds': r.bit_string.nmds,
                                           'url': reverse('bit_string',
                                                          kwargs={'b_id': r.bit_string.bit_string})
                                           },
                                       })

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@json_response
def record_search_aggregation(request):
    if request.method =='GET':
        start_age = request.GET.get('start',1)
        end_age = request.GET.get('end',120)
        gender = request.GET.get('gender','0')
        page = request.GET.get('p',1)
        kwargs = {}
        if gender == 'Male':
            gender = '1'
        elif gender == 'Female':
            gender = '2'
        if gender != '0':
            print gender
            kwargs['record__gender'] = gender
        country = request.GET.getlist('country','0')
        education = request.GET.get('education','0')
        if education != '0':
            kwargs['record__education'] = education
        if country != ['0']:
            kwargs['record__country__in'] = country
    print kwargs
    result = BitString.objects.filter(record__age__range=(start_age,end_age),**kwargs).annotate(num=Count('record'))
    objects  = Paginator(result,2000)
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
    return response_data


def record(request, record_id):
    r = Record.objects.get(id=record_id)
    response_data = {}
    response_data['result'] = 'success'
    response_data['data'] = {'age': r.age, 'gender': r.get_gender_display(),
                             'country': {'id': r.country, 'name': r.get_country_display() },
                             'education': {'level': r.education, 'name': r.get_education_display()},
                             'bitstring': {'value': r.bit_string.bit_string,
                                           'pca': r.bit_string.pca,
                                           'mds': r.bit_string.mds,
                                           'nmds': r.bit_string.nmds,
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

@json_response
def test(request):
    data = {"data": {"bitstrings": [{"count": 4221, "bitstring": {"origin": "0000111001010001", "mds": "0.0397458999459,0.183315153933", "pca": "-0.0792982586445,0.159979700251", "nmds": "0.0165809915404,0.0509848185975"}}]}}
    t = {
    "firstName": "John",
    "lastName": "Smith",
    "isAlive": True,
    "age": 25,
    "height_cm": 167.64,
    "address": {
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": "10021-3100"
    },
    "phoneNumbers": [
        { "type": "home", "number": "212 555-1234" },
        { "type": "fax",  "number": "646 555-4567" }
    ]
}
    return t
