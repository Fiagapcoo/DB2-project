from django.shortcuts import render, HttpResponse, redirect
from .models import *
# Create your views here.

def index(request):
    #check if the user is authenticated if so render the home page
    return redirect('login')


def login(request):
    return render(request, 'login.html')