from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import *
from django.db import connection
from .mock_data import PRODUCTS
from django.http import JsonResponse
import urllib.parse

def index(request):
    try:
        # Check if user is authenticated
        if request.session.get('user_id') and request.session.get('user_name'):

            categories = []
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM static_content.categories")
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                categories = [dict(zip(columns, row)) for row in rows]
            context = {
                'categories': categories,
            }
            
            return render(request, 'store.html', context)
        else:
            return redirect('login')
            
    except KeyError as e:
        print(f"Session key error: {str(e)}")
        return redirect('login')
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        # You might want to redirect to an error page in production
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def product_card(request):
    return render(request, 'product_card.html')

def instruments(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM dynamic_content.products p JOIN dynamic_content.stock s ON s.productid = p.productid  WHERE p."ProductType" = \'instrument\'')
        columns = [col[0] for col in cursor.description]
        instruments = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."ProductType" = \'instrument\');')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    context = {'instruments': instruments, 'categories': categories}
    return render(request, 'instruments.html', context)

def store(request):
    return render(request, 'store.html')

def top_bar(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."ProductType" = \'instrument\');')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    context = {'categories': categories}
    print(categories)
    return render(request, 'top_bar.html', context)

def top_bar_discount(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p.discountedprice IS NOT NULL);')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    context = {'categories': categories}
    print(categories)
    return render(request, 'top_bar_discount.html', context)

def top_bar_accessories(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."ProductType" = \'accessories\';')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    context = {'categories': categories}
    print(categories)
    return render(request, 'top_bar_accessories.html', context)

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
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM dynamic_content.products p JOIN dynamic_content.stock s ON s.productid = p.productid  WHERE p."ProductType" = \'accessories\'')
        columns = [col[0] for col in cursor.description]
        accessories = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."ProductType" = \'accessories\');')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    context = {'accessories': accessories, 'categories': categories}
    return render(request, 'accessories.html', context)

def discount(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM dynamic_content.products p JOIN dynamic_content.stock s ON s.productid = p.productid  WHERE p.discountedprice IS NOT null')
        columns = [col[0] for col in cursor.description]
        produtos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p.discountedprice IS NOT NULL);')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    context = {'produtos': produtos, 'categories': categories}
    return render(request, 'discount.html', context)

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


def checkout(request, product_id):
   with connection.cursor() as cursor:
       cursor.execute('SELECT * FROM dynamic_content.products WHERE "productid" = %s', [product_id])
       columns = [col[0] for col in cursor.description]
       product = dict(zip(columns, cursor.fetchone()))
   
   context = {'product': product}
   return render(request, 'checkout.html', context)

def cart(request):
    # Example cart data
    cart_items = [
        {"name": "Guitarra Elétrica", "quantity": 1, "unit_price": 500.00, "total_price": 500.00},
        {"name": "Pedal de Efeitos", "quantity": 2, "unit_price": 150.00, "total_price": 300.00},
    ]
    cart_subtotal = sum(item["total_price"] for item in cart_items)
    cart_tax = cart_subtotal * 0.23  # Example: 23% tax
    cart_total = cart_subtotal + cart_tax

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "cart_subtotal": cart_subtotal,
        "cart_tax": cart_tax,
        "cart_total": cart_total,
    })
    
# views.py
from django.shortcuts import render
from django.db import connection

def category_detail(request, id):
    with connection.cursor() as cursor:
        # Get products with stock information
        cursor.execute('''
            SELECT * FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid 
            WHERE p.categoryid = %s AND p."ProductType" = \'instrument\'
        ''', [id])
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Get category name
        cursor.execute('''
            SELECT name FROM static_content.categories c 
            WHERE categoryid = %s
        ''', [id])
        category_name = cursor.fetchone()
        
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."ProductType" = \'instrument\');')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    context = {
        'products': products, 
        'category_name': category_name[0] if category_name else '',
        'categories': categories
    }
    return render(request, 'category_detail.html', context)

def category_detail_discount(request, id):
    with connection.cursor() as cursor:
        # Get products with stock information
        cursor.execute('''
            SELECT * FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid 
            WHERE p.categoryid = %s AND p.discountedprice IS NOT null
        ''', [id])
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Get category name
        cursor.execute('''
            SELECT name FROM static_content.categories c 
            WHERE categoryid = %s
        ''', [id])
        category_name = cursor.fetchone()
        
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p.discountedprice IS NOT NULL);')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    context = {
        'products': products, 
        'category_name': category_name[0] if category_name else '',
        'categories': categories
    }
    return render(request, 'category_detail_discount.html', context)

def category_detail_accessories(request, id):
    with connection.cursor() as cursor:
        # Get products with stock information
        cursor.execute('''
            SELECT * FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid 
            WHERE p.categoryid = %s AND p."ProductType" = \'accessories\'
        ''', [id])
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Get category name
        cursor.execute('''
            SELECT name FROM static_content.categories c 
            WHERE categoryid = %s
        ''', [id])
        category_name = cursor.fetchone()
        
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."ProductType" = \'accessories\');')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    context = {
        'products': products, 
        'category_name': category_name[0] if category_name else '',
        'categories': categories
    }
    return render(request, 'category_detail_accessories.html', context)

def product_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT * FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid 
            WHERE p.productid = %s
        ''', [id])
        columns = [col[0] for col in cursor.description]
        product = dict(zip(columns, cursor.fetchone()))
        
        cursor.execute('SELECT * FROM static_content.categories')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    context = {'product': product, 'categories': categories}
    return render(request, 'product_detail.html', context)


def add_to_cart(request, id):
    cart = request.COOKIES.get('cart', '')
    cart = cart.split(',') if cart else []
    if str(id) not in cart:
        cart.append(str(id))
    cart = ','.join(cart)
    response = JsonResponse({'message': 'Product added to cart', 'cart': cart})
    response.set_cookie('cart', cart)
    return response


def admin(request):
    return render(request, 'admin.html')

from django.http import JsonResponse
from django.db import connection

def get_cart_items(request):
    product_ids = request.GET.get('ids', '')

    if not product_ids:
        return JsonResponse({"products": []})

    # 🔹 Decodifica a URL corretamente e substitui "\054" por ","
    product_ids = urllib.parse.unquote(product_ids).replace('\\054', ',')
    product_ids = [id.strip('"') for id in product_ids.split(',') if id.strip('"').isdigit()]  # Remover aspas extras

    if not product_ids:
        return JsonResponse({"products": []})

    placeholders = ','.join(['%s'] * len(product_ids))

    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT 
                p.productid, 
                p.name, 
                COALESCE(p.discountedprice, p.baseprice) AS final_price, 
                p.image_url, 
                s.quantity
            FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid 
            WHERE p.productid IN ({placeholders})
        ''', product_ids)

        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return JsonResponse({"products": products})

def remove_from_cart(request, id):
    if not id:
        return JsonResponse({'error': 'ID do produto inválido'}, status=400)

    cart = request.COOKIES.get('cart', '')

    if not cart:
        return JsonResponse({'message': 'Carrinho já está vazio', 'cart': ''})

    cart = cart.split(',')

    if str(id) in cart:
        cart.remove(str(id))

    new_cart = ','.join(cart)

    response = JsonResponse({'message': 'Produto removido do carrinho', 'cart': new_cart})
    response.set_cookie('cart', new_cart, path='/', max_age=31536000)  

    return response