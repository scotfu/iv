#!/usr/bin/env python
#coding=utf-8
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Count, Avg, Max

from .models import Record,BitString
from .distance import KMeans

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
        except Exception as e:
            print e
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    
    return decorator

@json_response
def record_search(request):
    if request.method =='GET':
        start_age = request.GET.get('start',1)
        end_age = request.GET.get('end',120)
        gender = request.GET.get('gender','0')
        page = request.GET.get('p',1)
        bit_string = request.GET.get('bit',None)
        kwargs = {}
        if gender == 'Male':
            gender = '1'
        elif gender == 'Female':
            gender = '2'
        if gender != '0':
            kwargs['gender'] = gender
        country = request.GET.get('country','0')
        education = request.GET.get('education','0')
        if education != '0':
            kwargs['education'] = education
        if country != '0':
            kwargs['country__in'] = country.split(",")
        if bit_string:
            kwargs['bit_string__bit_string'] = bit_string

    result = Record.objects.filter(age__range=(start_age,end_age),**kwargs)
    suggs = Record.objects.filter(age__range=(start_age,end_age),**kwargs).values("suggested_priority").distinct()
    
    objects  = Paginator(result,5000)
    response_data = {}
    response_data['result'] = 'success'
    response_data['p_num'] = objects.num_pages
    response_data['p'] = page
    response_data['data'] = {}
    response_data['data']['records'] = []
    response_data['suggs'] =[]
    for s in suggs:
            response_data['suggs'].append(s["suggested_priority"])
    
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

    return response_data

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
            kwargs['record__gender'] = gender
        country = request.GET.get('country',"0")
        education = request.GET.get('education','0')
        if education != '0':
            kwargs['record__education'] = education
        if country != '0':
            kwargs['record__country__in'] = country.split(",")
    print kwargs,country
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


@json_response
def record_search_group(request):
    if request.method =='GET':
        start_age = request.GET.get('start',1)
        end_age = request.GET.get('end',120)
        group_by = request.GET.get('group_by','0')
        kwargs = {}
        if group_by == 'gender':
            education = request.GET.get('education','0')
            if education != '0':
                kwargs['record__education'] = education
 
        elif group_by == 'education':
            gender =request.GET.get('gender','0')
            if gender == 'Male':
                gender = '1'
            elif gender == 'Female':
                gender = '2'
            if gender != '0':
                kwargs['record__gender'] = gender
        country = request.GET.get('country',0)
        if country != '0':
            kwargs['record__country__in'] = country.split(",")
    response_data = {}
    response_data['result'] = 'success'
    response_data['data'] = {}
            
    if group_by == 'gender':
        result_male = BitString.objects.filter(record__age__range=(start_age,end_age),record__gender=1,**kwargs).values('bit_string','nmds').annotate(num=Count('record'))
        result_female = BitString.objects.filter(record__age__range=(start_age,end_age),record__gender=2,**kwargs).values('bit_string','nmds').annotate(num=Count('record'))
        response_data['data']['female']=[]
        response_data['data']['male']=[]
        for r in result_male:
            response_data['data']['male'].append({
                'bitstring': {'origin': r["bit_string"],
                              'nmds': r["nmds"],
                                           },
                             'count': r["num"],
                             })

        for r in result_female:
            response_data['data']['female'].append({
                'bitstring': {'origin': r["bit_string"],
                              'nmds': r["nmds"],
                                           },
                             'count': r["num"],
                             })
    
        return response_data


    if group_by == 'edu':
        result1 = BitString.objects.filter(record__age__range=(start_age,end_age),record__education=1,**kwargs).values('record__gender','bit_string','nmds').annotate(num=Count('record'))
        result2 = BitString.objects.filter(record__age__range=(start_age,end_age),record__education=2,**kwargs).values('record__gender','bit_string','nmds').annotate(num=Count('record'))
        result3 = BitString.objects.filter(record__age__range=(start_age,end_age),record__education=3,**kwargs).values('record__gender','bit_string','nmds').annotate(num=Count('record'))
        result4 = BitString.objects.filter(record__age__range=(start_age,end_age),record__education=4,**kwargs).values('record__gender','bit_string','nmds').annotate(num=Count('record'))
        response_data['data']['edu1']=[]
        response_data['data']['edu2']=[]
        response_data['data']['edu3']=[]
        response_data['data']['edu4']=[]
        for r in result1:
            response_data['data']['edu1'].append({
                'bitstring': {'origin': r["bit_string"],
                              'nmds': r["nmds"],
                                           },
                             'count': r["num"],
                             })
        for r in result2:
            response_data['data']['edu2'].append({
                'bitstring': {'origin': r["bit_string"],
                              'nmds': r["nmds"],
                                           },
                             'count': r["num"],
                             })
        for r in result3:
            response_data['data']['edu3'].append({
                'bitstring': {'origin': r["bit_string"],
                              'nmds': r["nmds"],
                                           },
                             'count': r["num"],
                             })
        for r in result4:
            response_data['data']['edu4'].append({
                'bitstring': {'origin': r["bit_string"],
                              'nmds': r["nmds"],
                                           },
                             'count': r["num"],
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
def kmeans(request):
    if request.method =='GET':
        start_age = request.GET.get('start',1)
        end_age = request.GET.get('end',120)
        gender = request.GET.get('gender','0')
        algorithm = request.GET.get('algorithm','0')
        page = request.GET.get('p',1)
        kwargs = {}
        if gender == 'Male':
            gender = '1'
        elif gender == 'Female':
            gender = '2'
        if gender != '0':
            kwargs['record__gender'] = gender
        country = request.GET.get('country',"0")
        education = request.GET.get('education','0')
        if education != '0':
            kwargs['record__education'] = education
        if country != '0':
            kwargs['record__country__in'] = country.split(",")
        selected_points = set(request.GET.getlist("point"))
    selected_points = [map(float,getattr(BitString.objects.filter(bit_string=point)[0],algorithm).split(',')) for point in selected_points]     
    result = BitString.objects.filter(record__age__range=(start_age,end_age),**kwargs).annotate(num=Count('record'))

#    print avg
    objects  = Paginator(result,2000)
    response_data = {}
    response_data['result'] = 'success'
    response_data['p_num'] = objects.num_pages
    response_data['p'] = page
    response_data['data'] = {}
    response_data['centroids_sizes']=[]
    try :
        object_list = objects.page(page)
    except:
        response_data['p'] = 1
        object_list = records.page(1)
    points = [map(float,getattr(r,algorithm).split(',')) for r in object_list]
    cluster_matrix,centroids = KMeans(points,centroids=selected_points)
    for i in range(len(selected_points)):
        response_data['data']['group'+ str(i)] = []
    response_data['centroids']= {}

    for position in range(len(object_list)):
        r = object_list[position]
        k = 0
        while True:
            if cluster_matrix[k][position] == 1:
                break
            else:
                k += 1
        group_name = 'group'+ str(k)                
        response_data['data'][group_name].append({
                             'bitstring': {'origin': r.bit_string,
                                           'pca': r.pca,
                                           'mds': r.mds,
                                           'nmds': r.nmds,
                                           },
                             'count': r.num,
                             })
    for group in response_data['data']:
        response_data['centroids'][group] ={'avg_count':sum([record['count'] for record in response_data['data'][group]])/len(response_data['data'][group]), 'coordinate':centroids[int(group[-1])]}
    return response_data
    


@json_response
def kmeans_2(request):
    if request.method =='GET':
        start_age = request.GET.get('start',1)
        end_age = request.GET.get('end',120)
        gender = request.GET.get('gender','0')
        algorithm = request.GET.get('algorithm','0')
        page = request.GET.get('p',1)
        kwargs = {}
        if gender == 'Male':
            gender = '1'
        elif gender == 'Female':
            gender = '2'
        if gender != '0':
            kwargs['record__gender'] = gender
        country = request.GET.get('country',"0")
        education = request.GET.get('education','0')
        if education != '0':
            kwargs['record__education'] = education
        if country != '0':
            kwargs['record__country__in'] = country.split(",")
        selected_points_b = set(request.GET.getlist("point"))
        second_selected_points_b = list(set(request.GET.getlist("2nd_point")))
    selected_points = [map(float,getattr(BitString.objects.filter(bit_string=point)[0],algorithm).split(',')) for point in selected_points_b]
    second_selected_points = [map(float,getattr(BitString.objects.filter(bit_string=point)[0],algorithm).split(',')) for point in second_selected_points_b]     
    result = list(BitString.objects.filter(record__age__range=(start_age,end_age),**kwargs).annotate(num=Count('record')))
    response_data = {}
    response_data['result'] = 'success'
    response_data['data'] = {}
#    response_data['centroids_sizes']=[]
    points = [map(float,getattr(r,algorithm).split(',')) for r in result]
    cluster_matrix,centroids = KMeans(points,centroids=selected_points)

    
    one_point = second_selected_points_b[0]
#    print result
    point_position = result.index(BitString.objects.filter(bit_string=one_point)[0])
    tmp_k = 0
    while True:
        if cluster_matrix[tmp_k][point_position] == 1:
            break
        else:
            tmp_k += 1
    result = [result[i] for i in range(len(result)) if cluster_matrix[tmp_k][i]==1]            
    points = [map(float,getattr(r,algorithm).split(',')) for r in result]

    cluster_matrix,centroids = KMeans(points,centroids=second_selected_points)
    
    for i in range(len(second_selected_points)):
        response_data['data']['group'+ str(i)] = []
    response_data['centroids']= {}

    for position in range(len(result)):
        r = result[position]
        k = 0
        while True:
            if cluster_matrix[k][position] == 1:
                break
            else:
                k += 1
        group_name = 'group'+ str(k)                
        response_data['data'][group_name].append({
                             'bitstring': {'origin': r.bit_string,
                                           'pca': r.pca,
                                           'mds': r.mds,
                                           'nmds': r.nmds,
                                           },
                             'count': r.num,
                             })
    for group in response_data['data']:
        response_data['centroids'][group] ={'avg_count':sum([record['count'] for record in response_data['data'][group]])/len(response_data['data'][group]), 'coordinate':centroids[int(group[-1])]}
    return response_data
    




    
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
