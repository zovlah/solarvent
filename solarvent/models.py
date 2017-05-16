#!/usr/bin/env python
# -*- coding: utf8 -*- 
# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Proizvodjac(models.Model):
    naziv = models.CharField(max_length=128, verbose_name=u'Naziv proizvođača')
    
    class Meta:
        ordering = ['naziv']
    
    def __str__(self):
        return self.naziv
    
@python_2_unicode_compatible
class Proizvod_main(models.Model):
    proizvod = models.CharField(max_length=128, verbose_name=u'Naziv proizvoda')

    class Meta:
        ordering = ['proizvod']

    def __str__(self):
        return self.proizvod
    
        

@python_2_unicode_compatible
class Proizvod_opis(models.Model):
    proizvod_main = models.ForeignKey(Proizvod_main)
    proizvodjac = models.ForeignKey(Proizvodjac)
    opis = models.CharField(max_length=128, verbose_name=u'Opis proizvoda')
    model = models.CharField(max_length=128, verbose_name=u'Model' )
    
    class Meta:
        ordering = ['opis']
    
    def __str__(self):
        return "%s, %s" %(self.opis, self.model)
        

@python_2_unicode_compatible
class Proizvod_model(models.Model):
    proizvod_opis = models.ForeignKey(Proizvod_opis)
    model_detalj = models.CharField(max_length=32, verbose_name=u'Model detalj')
    
    class Meta:
        ordering = ['model_detalj']
    
    def __str__(self):
        return self.model_detalj
    
@python_2_unicode_compatible
class Proizvod_dimenzija(models.Model):
    proizvod_model = models.ForeignKey(Proizvod_model)
    tezina = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'kg')
    duzina = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'mm')
    sirina = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'mm')
    visina = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'mm')
    max_snaga = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'W')
    
    def __str__(self):
        return u"težina=%0.2f, dužina=%0.2f, širina=%0.2f, visina=%0.2f" %(self.tezina, self.duzina, self.sirina, self.visina)
    

    
@python_2_unicode_compatible
class Proizvod_rezim(models.Model):
    proizvod_model = models.ForeignKey(Proizvod_model)
    rezim_opis = models.CharField(max_length=128, verbose_name=u'Naziv režima')
    
    def __str__(self):
        return self.rezim_opis
    
class Rezim_det(models.Model):
    proizvod_rezim = models.ForeignKey(Proizvod_rezim)
    brzina = models.CharField(max_length=64)
    voda_ulaz = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'EWT°C')
    voda_izlaz = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'LWT°C')
    voda_protok = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'l/s')
    voda_pad_tlaka = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'kPa')
    zrak_protok = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'm3/h')
    rash_ucin = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'W', null=True, blank=True)
    osjetni_ucin = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'W', null=True, blank=True)
    zrak_izlaz = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'LAT°C')
    zvucni_tlak = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'dB(A)')
    zvucna_snaga= models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'dB(A)')
    ucin_grijanja = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'W', null=True, blank=True)
    el_snaga = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'W')
    
