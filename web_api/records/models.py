#! /usr/bin/env python
#coding=utf-8
from django.db import models
from utils.constant import COUNTRY

GENDER = (
        ('1', 'Male'),
        ('2', 'Female'),
        )
EDUCATION = (
        ('1' , "Some primary"),
        ('2' , "Finished primary"),
        ('3' , "Some secondary"),
        ('4' , "Finished secondary"),
        )

class Record(models.Model):


    age = models.IntegerField()
    gender = models.CharField(max_length=100,choices=GENDER)
    education = models.CharField(max_length=100,choices=EDUCATION)
    bit_string = models.ForeignKey('BitString')
    country = models.CharField(max_length=100,choices=COUNTRY)
    suggested_priority = models.TextField()
    
    def __unicode__(self):
        return self.bit_string.bit_string

    class Meta:
        verbose_name_plural = "Records"

class BitString(models.Model):
    bit_string = models.CharField(max_length=100)
    pca =models.CharField(max_length=200)
    mds =models.CharField(max_length=200)
    nmds =models.CharField(max_length=200)

    def __unicode__(self):
        return self.bit_string
