from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import *
from django.db import connection
from .mock_data import PRODUCTS

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

def instruments(request):
    return render(request, 'instruments.html')

def store(request):
    return render(request, 'store.html')

def top_bar(request):
    return render(request, 'top_bar.html')

def navbar(request):
    return render(request, 'navbar.html')

def brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    return render(request, 'brand.html', {'brand': brand})

def filter_card(request):
    return render(request, 'filter_card.html')

def product_details(request):
    return render(request, 'product_details.html')

def brand_details(request):
    return render(request, 'brand_details.html')

def base(request):
    return render(request, 'base.html')

def payment_details(request):
    return render(request, 'payment_details.html')

def brands_page(request):
    return render(request, 'brands_page.html')

def new(request):
    return render(request, 'new.html', {'products': PRODUCTS})

def highlights(request):
    return render(request, 'highlights.html')

def accessories(request):
    return render(request, 'accessories.html')

def discount(request):
    return render(request, 'discount.html')

def delete_product(request, product_id):
    # Logic for deleting the product goes here
    return HttpResponse(f"Delete product with ID: {product_id}")

def add_to_basket(request, product_id):
    # Placeholder for adding the product to the basket
    return HttpResponse(f"Product {product_id} added to basket!")

def edit_product(request, product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product is None:
        return render(request, '404.html')  # Produto não encontrado.
    
    thumbnails = range(4)  # Gera uma lista de números [0, 1, 2, 3].
    return render(request, 'edit_product.html', {'product': product, 'thumbnails': thumbnails})

  def order_history(request):
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    user_id = request.session['user_id']
    user_orders = []

    with connection.cursor() as cursor:

        cursor.execute("SELECT * FROM transactions.orders WHERE userid = %s;", [user_id])
        user_orders = cursor.fetchall()
    

    context = {'user_orders': user_orders}
    return render(request, 'order_history.html', context)

def logout(request):
    request.session.flush()
    return redirect('login')

  def order_history(request):
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    user_id = request.session['user_id']
    user_orders = []

    with connection.cursor() as cursor:

        cursor.execute("SELECT * FROM transactions.orders WHERE userid = %s;", [user_id])
        user_orders = cursor.fetchall()
    

    context = {'user_orders': user_orders}
    return render(request, 'order_history.html', context)

def logout(request):
    request.session.flush()
    return redirect('login')