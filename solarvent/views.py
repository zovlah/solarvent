#!/usr/bin/env python
# -*- coding: utf8 -*- 
# coding: utf-8

from __future__ import unicode_literals

from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Proizvod_main, Proizvod_opis, Proizvod_model, Proizvod_rezim, Proizvod_dimenzija, Rezim_det
from django.http import Http404, HttpResponse
import csv
from django.utils.timezone import localtime
from django.utils import timezone
from django.forms.models import model_to_dict


# Create your views here.

def index(request):
    
    proizvodi_main_list = Proizvod_main.objects.all()
    context = {'proizvodi_list' : proizvodi_main_list} 
    
    return render(request,'proizvodi.html', context)


def proizvod_opis(request, proizvod_opis_id):
    
    proizvod_list = get_list_or_404(Proizvod_opis, proizvod_main=proizvod_opis_id)

    context = {'proizvod_list' : proizvod_list}
    
    return render(request,'proizvod_opis.html', context)

def proizvod_model(request, proizvod_opis_id):
    
    proizvod_list = get_list_or_404(Proizvod_model, proizvod_opis=proizvod_opis_id)
        
    context = {'proizvod_list' : proizvod_list}
    
    return render(request,'proizvod_model.html', context)

def model_rezim(request, model_id):
    
    rezim_list = get_list_or_404(Proizvod_rezim, proizvod_model=model_id)
        
    context = {'rezim_list' : rezim_list}
    
    return render(request,'model_rezim.html', context)


def rezim_det_dim(request, rezim_id):
    """Namjerno nije stavljeno get_or_404 jer to vraca listu pa ne radi citanje verbose name u templateu"""
    rezim_list = Rezim_det.objects.filter(proizvod_rezim=rezim_id)
    if not rezim_list:
        raise Http404(u"Ne pronalazi ništa u Rezim_det tablici.")
    
    try:
        dimenzije = Proizvod_dimenzija.objects.get(proizvod_model = rezim_list[0].proizvod_rezim.proizvod_model)
    except Proizvod_dimenzija.DoesNotExist:
        raise Http404("Ne pronalazi dimenzije za model u tablici Proizvod_dimenzija.")
    
#    dimenzije = get_object_or_404(Proizvod_dimenzija, proizvod_model = rezim_list[0].proizvod_rezim.proizvod_model)
    
    context = {'rezim_list' : rezim_list,
               'dimenzije' : dimenzije}
    
    return render(request,'rezim_det_dim.html', context)

def trailing_zeroes(broj):
    s = str(broj)
    if '.' in s:
        s = s.rstrip('0')
        
    if s.endswith('.'):
        s = s[:-1]
    
    return s

def csv_generetor_dot(request, rezim_id):
    
    rezim = get_object_or_404(Proizvod_rezim, pk=rezim_id)
    proizvod_model = rezim.proizvod_model
    dimenzija = Proizvod_dimenzija.objects.get(proizvod_model=proizvod_model)
    
    # Create the HttpResponse object with the appropriate CSV header.
    proizvod_model = proizvod_model.model_detalj
    proizvod_model = proizvod_model.replace(' ', '_')
    
    time_stamp_raw = localtime(timezone.now()) 
    time_stamp = time_stamp_raw.strftime("%d_%m_%Y_%H_%M_%S")
    
    filaname = proizvod_model + '_dot_' + time_stamp + '.csv'
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' %filaname

    writer = csv.writer(response, delimiter=str(u';').encode('utf-8'))
    
    rezim_det_list = Rezim_det.objects.filter(proizvod_rezim = rezim)
    
    if 'lađenje' in rezim.rezim_opis:
        writer.writerow(['tezina', 'duzina', 'sirina', 'visina', 'max_snaga', 'brzina', 'voda_ulaz', 'voda_izlaz', 'voda_protok', 'voda_pad_tlaka',
                         'zrak_izlaz', 'zrak_protok', 'rashladni_ucin', 'osjetni_ucin', 'zvucni_tlak', 'zvucna_snaga', 'el_snaga'])
        for obj in rezim_det_list:
            writer.writerow([trailing_zeroes(dimenzija.tezina), trailing_zeroes(dimenzija.duzina), trailing_zeroes(dimenzija.sirina), 
                             trailing_zeroes(dimenzija.visina), trailing_zeroes(dimenzija.max_snaga),
                             trailing_zeroes(obj.brzina), trailing_zeroes(obj.voda_ulaz), trailing_zeroes(obj.voda_izlaz), 
                             trailing_zeroes(obj.voda_protok), trailing_zeroes(obj.voda_pad_tlaka),
                             trailing_zeroes(obj.zrak_izlaz), trailing_zeroes(obj.zrak_protok), trailing_zeroes(obj.rash_ucin), 
                             trailing_zeroes(obj.osjetni_ucin), trailing_zeroes(obj.zvucni_tlak), trailing_zeroes(obj.zvucna_snaga), 
                             trailing_zeroes(obj.el_snaga)])
    elif 'rijanje' in rezim.rezim_opis:
        for obj in rezim_det_list:
            writer.writerow([trailing_zeroes(dimenzija.tezina), trailing_zeroes(dimenzija.duzina), trailing_zeroes(dimenzija.sirina), 
                             trailing_zeroes(dimenzija.visina), trailing_zeroes(dimenzija.max_snaga),
                             trailing_zeroes(obj.brzina), trailing_zeroes(obj.voda_ulaz), trailing_zeroes(obj.voda_izlaz), 
                             trailing_zeroes(obj.voda_protok), trailing_zeroes(obj.voda_pad_tlaka),
                             trailing_zeroes(obj.zrak_izlaz), trailing_zeroes(obj.zrak_protok), trailing_zeroes(obj.ucin_grijanja), 
                             trailing_zeroes(obj.zvucni_tlak), trailing_zeroes(obj.zvucna_snaga), trailing_zeroes(obj.el_snaga)])
    return response 


def dot_to_coma(broj):
    broj_str = trailing_zeroes(broj)
    broj_str = broj_str.replace('.', ',')
    return broj_str



def csv_generetor_coma(request, rezim_id):
    
    rezim = get_object_or_404(Proizvod_rezim, pk=rezim_id)
    proizvod_model = rezim.proizvod_model
    dimenzija = Proizvod_dimenzija.objects.get(proizvod_model=proizvod_model)
    
    # Create the HttpResponse object with the appropriate CSV header.
    proizvod_model = proizvod_model.model_detalj
    proizvod_model = proizvod_model.replace(' ', '_')
    
    time_stamp_raw = localtime(timezone.now()) 
    time_stamp = time_stamp_raw.strftime("%d_%m_%Y_%H_%M_%S")
    
    filaname = proizvod_model + '_coma_' + time_stamp + '.csv'
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' %filaname

    writer = csv.writer(response, delimiter=str(u';').encode('utf-8'))
    
    rezim_det_list = Rezim_det.objects.filter(proizvod_rezim = rezim)
    
    fields = ['tezina', 'duzina', 'sirina', 'visina', 'max_snaga']
    
    dimenzija_dict = model_to_dict(dimenzija, fields)
    
    for key, value in dimenzija_dict.iteritems():
        dimenzija_dict[key] = dot_to_coma(value)
        
    dimenzija_array = []
    dimenzija_array.append(dimenzija_dict['tezina'])
    dimenzija_array.append(dimenzija_dict['duzina'])
    dimenzija_array.append(dimenzija_dict['sirina'])
    dimenzija_array.append(dimenzija_dict['visina'])
    dimenzija_array.append(dimenzija_dict['max_snaga'])
    
     
        
    
    if 'lađenje' in rezim.rezim_opis:
        writer.writerow(['tezina', 'duzina', 'sirina', 'visina', 'max_snaga', 'brzina', 'voda_ulaz', 'voda_izlaz', 'voda_protok', 'voda_pad_tlaka',
                         'zrak_izlaz', 'zrak_protok', 'rashladni_ucin', 'osjetni_ucin', 'zvucni_tlak', 'zvucna_snaga', 'el_snaga'])
        for obj in rezim_det_list:
            writer.writerow(dimenzija_array + [dot_to_coma(obj.brzina), dot_to_coma(obj.voda_ulaz), dot_to_coma(obj.voda_izlaz), 
                            dot_to_coma(obj.voda_protok), dot_to_coma(obj.voda_pad_tlaka),
                            dot_to_coma(obj.zrak_izlaz), dot_to_coma(obj.zrak_protok), dot_to_coma(obj.rash_ucin), 
                            dot_to_coma(obj.osjetni_ucin), dot_to_coma(obj.zvucni_tlak), dot_to_coma(obj.zvucna_snaga), 
                            dot_to_coma(obj.el_snaga)])
            
    elif 'rijanje' in rezim.rezim_opis:
        for obj in rezim_det_list:
            writer.writerow([dimenzija.tezina, dimenzija.duzina, dimenzija.sirina, dimenzija.visina, dimenzija.max_snaga,
                             obj.brzina, obj.voda_ulaz, obj.voda_izlaz, obj.voda_protok, obj.voda_pad_tlaka,
                             obj.zrak_izlaz, obj.zrak_protok, obj.ucin_grijanja, obj.zvucni_tlak, obj.zvucna_snaga, obj.el_snaga])
    return response 

    