#!/usr/bin/env python
# -*- coding: utf8 -*- 
# coding: utf-8

from django import template
register = template.Library()

def get_field_verbose_name(instance, arg):
    return instance._meta.get_field(arg).verbose_name
register.filter('field_verbose_name', get_field_verbose_name)

def get_queryset_field_verbose_name(queryset, arg):
    return queryset.model._meta.get_field(arg).verbose_name
register.filter('queryset_field_verbose_name', get_queryset_field_verbose_name)