#!/usr/bin/env python
import csv
import sys
import logging
sys.path.append('/home/fu/workspaces/iv/web_api')

from django.conf import settings
from web_api.settings import local
from django.core.management import setup_environ
setup_environ(local)

from records.models import BitString,Record

error_logger = logging.getLogger('import_error')
info_logger = logging.getLogger('import_info')

def bit_init():
    f0 = open('coor.csv.2000').readlines()
    f = open('tmp_data.2000').readlines()#pca
    f1 = open('tmp_data1.2000').readlines()#mds
    f2 = open('tmp_data2.2000').readlines()#nmds

    n=0
    while n<2000:
        string = BitString()
        string.bit_string = ''.join(f0[n].strip().split(','))
        string.pca = f[n].strip()
        string.mds = f1[n].strip()
        string.nmds= f2[n].strip()
        n += 1
        string.save()
    f0.close()    
    f.close()
    f1.cose()
    f2.close()


def record_init():
    f = open('raw_data').readlines()
    f.pop(0)
    r_list=[]
    lineno = 0
    for line in f:
        lineno += 1
        try:
            line = line.strip().split(',')
            record = Record()
            record.country = int(line[1])
            record.age = int(line[2])
            record.gender = int(line[3])
            record.education = int(line[4])
            record.suggested_priority = line[6]
            b = BitString.objects.filter(bit_string=line[5])
            if b:
                record.bit_string = b[0]
                r_list.append(record)
            if len(r_list) >= 500:
                info_logger.info('save 500')
                Record.objects.bulk_create(r_list)
                r_list=[]
        except Exception,e:
            if r_list:
                Record.objects.bulk_create(r_list)
            r_list=[]
            error_logger.error(str(lineno))
    try:
        Record.objects.bulk_create(r_list)
    except Exception,e:
        logger.error(e)

if __name__ == '__main__':
    record_init()
