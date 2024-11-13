from django.shortcuts import render, HttpResponse
from .models import *
# Create your views here.

def index(request):
    products = Produtos.objects.all()
    return render(request, 'store.html', {'products': products})

def product_card(request):
    return render(request, 'product_card.html')

def top_bar(request):
    return render(request, 'top_bar.html')

def navbar(request):
    return render(request, 'navbar.html')

def brand(request):
    return render(request, 'brand.html')

def filter_card(request):
    return render(request, 'filter_card.html')

def product_details(request):
    return render(request, 'product_details.html')

def brand_details(request):
    return render(request, 'brand_details.html')

def base(request):
    return render(request, 'base.html')