from django.shortcuts import render, HttpResponse, redirect
from .models import *
# Create your views here.

def index(request):
    try:
        if request.session['user_id'] and request.session['user_name']:
            products = Produtos.objects.all()
            print (f"ID: {request.session['user_id']}")
            print (f"Name: {request.session['user_name']}")
            return render(request, 'store.html', {'products': products})
        else:
                return redirect('login')
    except KeyError:
        return redirect('login')    
    

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