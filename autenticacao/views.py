from django.shortcuts import render, HttpResponse
from .models import *
# Create your views here.

def login(request):
    return render(request, 'login.html')