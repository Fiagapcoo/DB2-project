from django.shortcuts import render, HttpResponse
from .models import *
# Create your views here.

def index(request):
    products = Produtos.objects.all()
    return render(request, 'store.html', {'products': products})