#!/usr/bin/env python
# -*- coding: utf8 -*- 
# coding: utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^proizvod_opis/(?P<proizvod_opis_id>\d+)/$', views.proizvod_opis, name='proizvod_opis'),
    url(r'^proizvod_model/(?P<proizvod_opis_id>\d+)/$', views.proizvod_model, name='proizvod_model'),
    url(r'^model_rezim/(?P<model_id>\d+)/$', views.model_rezim, name='model_rezim'),
    url(r'^rezim_det_dim/(?P<rezim_id>\d+)/$', views.rezim_det_dim, name='rezim_det_dim'),
    url(r'^csv_generetor_dot/(?P<rezim_id>\d+)/$', views.csv_generetor_dot, name='csv_generator_dot'),
    url(r'^csv_generetor_coma/(?P<rezim_id>\d+)/$', views.csv_generetor_coma, name='csv_generator_coma'),
    
]