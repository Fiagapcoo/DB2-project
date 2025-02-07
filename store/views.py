from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.core.paginator import Paginator
from django.db import connection
from .mock_data import PRODUCTS
from django.http import JsonResponse
import urllib.parse
from . import upload_to_cloudinary
import json
import random
from threading import Timer

def process_checkout(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)


    user_id = request.session.get("user_id")

    if not user_id:
        return JsonResponse({"error": "Usuário não autenticado"}, status=401)

    try:
        data = json.loads(request.body)


        cart_content = data.get("cart", {})
        total_amount = data.get("total", 0.00)
        payment_method = data.get("payment_method", "cash_on_delivery")


        address_line1 = data.get("address_line1", "")
        city = data.get("city", "")
        postal_code = data.get("postal_code", "")
        country = data.get("country", "")
        phone_number = data.get("phone_number", "")

        if not cart_content or total_amount <= 0:
            return JsonResponse({"error": "Carrinho vazio ou valor inválido"}, status=400)


        transaction_code = f"TXN{random.randint(10000, 99999)}"


        formatted_cart = {
            "items": [{"product_id": int(product_id), "quantity": quantity} for product_id, quantity in cart_content.items()]
        }

        with connection.cursor() as cursor:

            for item in formatted_cart["items"]:
                product_id = item["product_id"]
                quantity = item["quantity"]

                cursor.execute("SELECT quantity FROM dynamic_content.stock WHERE productid = %s", [product_id])
                stock = cursor.fetchone()

                if not stock or stock[0] < quantity:
                    return JsonResponse({"error": f"Estoque insuficiente para o produto {product_id} (disponível: {stock[0] if stock else 0})"}, status=400)
            
            cart_content_json = json.dumps(formatted_cart)

            cursor.execute("SELECT TRANSACTIONS.insert_order(%s, %s, %s);", (user_id, transaction_code, cart_content_json))

            order_id = cursor.fetchone()[0]


            cursor.execute("""
                INSERT INTO hr.user_address (userid, address_line1, city, postal_code, country, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING addressid
            """, (user_id, address_line1, city, postal_code, country, phone_number))

            address_id = cursor.fetchone()[0]


            cursor.execute("""
                INSERT INTO transactions.payments (orderid, userid, paymentmethod, paymentstatus, amount)
                VALUES (%s, %s, %s, %s, %s)
            """, (order_id, user_id, payment_method, "Pending", total_amount))


            if payment_method == "cash_on_delivery":

                for item in formatted_cart["items"]:
                    product_id = item["product_id"]
                    quantity = item["quantity"]

                    cursor.execute("""
                        UPDATE dynamic_content.stock
                        SET quantity = quantity - %s, lastupdated = now()
                        WHERE productid = %s
                    """, (quantity, product_id))

                print(f"🛒 Estoque atualizado imediatamente para o pedido {order_id} (Pagamento na Entrega).")

            elif payment_method == "bank_transfer":
                print(f"💰 Simulando pagamento para o pedido {order_id}...")

                def complete_payment():
                    with connection.cursor() as cursor:

                        cursor.execute("""
                            UPDATE transactions.payments
                            SET paymentstatus = 'Paid'
                            WHERE orderid = %s
                        """, [order_id])


                        cursor.execute("""
                            UPDATE transactions.orders
                            SET status = 'Completed'
                            WHERE orderid = %s
                        """, [order_id])


                        for item in formatted_cart["items"]:
                            product_id = item["product_id"]
                            quantity = item["quantity"]

                            cursor.execute("""
                                UPDATE dynamic_content.stock
                                SET quantity = quantity - %s, lastupdated = now()
                                WHERE productid = %s
                            """, (quantity, product_id))

                    print(f"✅ Pagamento confirmado e estoque atualizado para o pedido {order_id}!")

                Timer(30, complete_payment).start()

        return JsonResponse({
            "success": True,
            "message": "Pedido realizado com sucesso! Aguarde confirmação do pagamento...",
            "order_id": order_id,
            "transaction_code": transaction_code
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def index(request):
    try:
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

        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def product_card(request):
    return render(request, 'product_card.html')

def instruments(request):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT * FROM dynamic_content.instrument_products_with_stock;
        ''')
        columns = [col[0] for col in cursor.description]
        instruments = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.execute('''
            SELECT * FROM static_content.categories_with_instruments;
        ''')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(instruments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories
    }
    return render(request, 'instruments.html', context)

def store(request):
    try:
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
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def top_bar(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."producttype" = \'instrument\');')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    context = {'categories': categories}
    print(categories)
    return render(request, 'top_bar.html', context)

def navbar(request):
    return render(request, 'navbar.html')

def filter_card(request):
    categorias = Categoria.objects.all()
    return render(request, 'filter_card.html', {'categorias': categorias})

def base(request):
    return render(request, 'base.html')

def payment_details(request):
    return render(request, 'payment_details.html')

def new(request):
    category_id = request.GET.get('categoria', '')
    brand_id = request.GET.get('marca', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    stock_filter = request.GET.get('stock', '')
    search_query = request.GET.get('search', '')

    with connection.cursor() as cursor:

        cursor.execute("SELECT * FROM static_content.categories")
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT * FROM dynamic_content.latest_products_by_brand;
        """)
        columns = [col[0] for col in cursor.description]
        brands = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.execute("""
            select * FROM dynamic_content.product_price_range
        """)
        min_db_price, max_db_price = cursor.fetchone()

        if not min_price:
            min_price = min_db_price
        if not max_price:
            max_price = max_db_price

        query = '''
            SELECT p.*, s.quantity 
            FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid
        '''
        params = []


        
        
        if category_id:
            query += " AND p.categoryid = %s"
            params.append(category_id)

        if brand_id:
            query += " AND p.brandid = %s"
            params.append(brand_id)


        if min_price and max_price:
            query += " AND COALESCE(p.discountedprice, p.baseprice) BETWEEN %s AND %s"
            params.extend([min_price, max_price])


        if stock_filter == 'in_stock':
            query += " AND s.quantity > 0"
        elif stock_filter == 'out_of_stock':
            query += " AND s.quantity = 0"

        selected_discount = request.GET.get('desconto', '')

        if selected_discount == 'com_desconto':
            query += " AND p.discountedprice IS NOT NULL"
        elif selected_discount == 'sem_desconto':
            query += " AND p.discountedprice IS NULL"   

        if search_query:
            query += " AND (p.name ILIKE %s OR p.productserialnumber ILIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        query += " ORDER BY p.productid DESC LIMIT 20"

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
            'page_obj': page_obj,
            'categories': categories,
            'brands': brands,
            'selected_category': category_id,
            'selected_brand': brand_id,
            'min_price': min_price,
            'max_price': max_price,
            'min_db_price': min_db_price,
            'max_db_price': max_db_price,
            'selected_stock': stock_filter,
            'search_query': search_query,
            'selected_discount': selected_discount
        }
    return render(request, 'new.html', context)

def accessories(request):
    page_number = request.GET.get('page')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    stock_filter = request.GET.get('stock', '')
    search_query = request.GET.get('search', '')
    brand_id = request.GET.get('marca', '')
    discount_filter = request.GET.get('desconto', '')

    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT MIN(COALESCE(discountedprice, baseprice)), MAX(COALESCE(discountedprice, baseprice))
            FROM dynamic_content.products
            WHERE producttype = 'accessories'
        ''')
        min_db_price, max_db_price = cursor.fetchone()

        if not min_price:
            min_price = min_db_price
        if not max_price:
            max_price = max_db_price

        cursor.execute("""
            SELECT DISTINCT b.brandid, b.brandname
            FROM dynamic_content.products p
            JOIN dynamic_content.brands b ON p.brandid = b.brandid
            WHERE p.producttype = 'accessories'
            ORDER BY b.brandname
        """)
        columns = [col[0] for col in cursor.description]
        brands = [dict(zip(columns, row)) for row in cursor.fetchall()]

        query = '''
            SELECT p.*, s.quantity FROM dynamic_content.products p
            JOIN dynamic_content.stock s ON s.productid = p.productid
            WHERE p.producttype = 'accessories'
        '''
        params = []

        if brand_id:
            query += " AND p.brandid = %s"
            params.append(brand_id)

        if discount_filter == "com_desconto":
            query += " AND p.discountedprice IS NOT NULL"
        elif discount_filter == "sem_desconto":
            query += " AND p.discountedprice IS NULL"

        if min_price and max_price:
            query += " AND COALESCE(p.discountedprice, p.baseprice) BETWEEN %s AND %s"
            params.extend([min_price, max_price])

        if stock_filter == 'in_stock':
            query += " AND s.quantity > 0"
        elif stock_filter == 'out_of_stock':
            query += " AND s.quantity = 0"

        if search_query:
            query += " AND (p.name ILIKE %s OR p.productserialnumber ILIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        accessories = [dict(zip(columns, row)) for row in cursor.fetchall()]

    paginator = Paginator(accessories, 15)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'brands': brands,
        'selected_brand': brand_id,
        'min_price': min_price,
        'max_price': max_price,
        'min_db_price': min_db_price,
        'max_db_price': max_db_price,
        'selected_stock': stock_filter,
        'selected_discount': discount_filter,
        'search_query': search_query,
    }
    return render(request, 'accessories.html', context)

def discount(request):
    category_id = request.GET.get('categoria', '')
    brand_id = request.GET.get('marca', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    stock_filter = request.GET.get('stock', '')
    search_query = request.GET.get('search', '')

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM static_content.categories")
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT DISTINCT b.brandid, b.brandname
            FROM dynamic_content.products p
            JOIN dynamic_content.brands b ON p.brandid = b.brandid
            WHERE p.discountedprice IS NOT NULL
            ORDER BY b.brandname
        """)
        columns = [col[0] for col in cursor.description]
        brands = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.execute("SELECT MIN(discountedprice), MAX(discountedprice) FROM dynamic_content.products WHERE discountedprice IS NOT NULL")
        min_db_price, max_db_price = cursor.fetchone()

        if not min_price:
            min_price = min_db_price
        if not max_price:
            max_price = max_db_price

        query = '''
            SELECT p.*, s.quantity FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid  
            WHERE p.discountedprice IS NOT NULL
        '''
        params = []

        if category_id:
            query += " AND p.categoryid = %s"
            params.append(category_id)


        if brand_id:
            query += " AND p.brandid = %s"
            params.append(brand_id)


        if min_price and max_price:
            query += " AND p.discountedprice BETWEEN %s AND %s"
            params.extend([min_price, max_price])


        if stock_filter == 'in_stock':
            query += " AND s.quantity > 0"
        elif stock_filter == 'out_of_stock':
            query += " AND s.quantity = 0"
        if search_query:
            query += " AND (p.name ILIKE %s OR p.productserialnumber ILIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        produtos = [dict(zip(columns, row)) for row in cursor.fetchall()]


    paginator = Paginator(produtos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'selected_category': category_id,
        'selected_brand': brand_id,
        'min_price': min_price,
        'max_price': max_price,
        'min_db_price': min_db_price,
        'max_db_price': max_db_price,
        'selected_stock': stock_filter,
        'search_query': search_query, 
        'is_discount_page': True 
    }
    return render(request, 'discount.html', context)


def edit_product(request, product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product is None:
        return render(request, '404.html')
    
    thumbnails = range(4)
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

def order_details(request, order_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM transactions.orders WHERE orderid = %s", [order_id])
        order = cursor.fetchone()

        cursor.execute("SELECT paymentmethod, amount FROM transactions.payments WHERE orderid = %s", [order_id])
        payment = cursor.fetchone()

        cursor.execute("""
            SELECT ua.address_line1, ua.address_line2, ua.city, ua.postal_code, ua.country, ua.phone_number, u.name, u.email
            FROM hr.user_address ua
            JOIN hr.users u ON ua.userid = u.userid
            WHERE ua.userid = %s
            ORDER BY ua.addressid DESC LIMIT 1
        """, [order[1]]) 

        address = cursor.fetchone()

    if order:
        try:
            items_data = order[4]
            if isinstance(items_data, str):  
                items_data = json.loads(items_data)  

            order_data = {
                "id": order[0],
                "transaction_code": order[2],
                "status": order[3],
                "items": items_data["items"],
                "payment_method": payment[0] if payment else "Desconhecido",
                "amount": payment[1] if payment else "0.00",
                "address": {
                    "line1": address[0] if address else "N/A",
                    "line2": address[1] if address and address[1] else "",
                    "city": address[2] if address else "N/A",
                    "postal_code": address[3] if address else "N/A",
                    "country": address[4] if address else "N/A",
                    "phone_number": address[5] if address else "N/A",
                },
                "user_info": {
                    "name": address[6] if address else "N/A",
                    "email": address[7] if address else "N/A"
                }
            }
        except (json.JSONDecodeError, KeyError, TypeError):
            order_data = {"id": order[0], "transaction_code": order[2], "status": order[3], "items": []}
    else:
        order_data = None

    return render(request, 'order_details.html', {"order": order_data})

def logout(request):
    request.session.flush()
    response = redirect('login')
    response.delete_cookie('cart')
    return response

def checkout(request, product_id):
   with connection.cursor() as cursor:
       cursor.execute('SELECT * FROM dynamic_content.products WHERE "productid" = %s', [product_id])
       columns = [col[0] for col in cursor.description]
       product = dict(zip(columns, cursor.fetchone()))
   
   context = {'product': product}
   return render(request, 'checkout.html', context)

def cart(request):
    return render(request, "cart.html")
 
def category_detail(request, id):
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    stock_filter = request.GET.get('stock', '')
    search_query = request.GET.get('search', '')
    brand_id = request.GET.get('marca', '')
    discount_filter = request.GET.get('desconto', '')

    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM static_content.categories WHERE categoryid = %s", [id])
        category_name = cursor.fetchone()

        if category_name:
            category_name = category_name[0]
        else:
            category_name = "Categoria Desconhecida"

        cursor.execute('''
            SELECT MIN(COALESCE(discountedprice, baseprice)), MAX(COALESCE(discountedprice, baseprice)) 
            FROM dynamic_content.products 
            WHERE categoryid = %s
        ''', [id])
        min_db_price, max_db_price = cursor.fetchone()

        if not min_price:
            min_price = min_db_price
        if not max_price:
            max_price = max_db_price

        cursor.execute("""
            SELECT DISTINCT b.brandid, b.brandname 
            FROM dynamic_content.products p 
            JOIN dynamic_content.brands b ON p.brandid = b.brandid 
            WHERE p.categoryid = %s
            ORDER BY b.brandname
        """, [id])
        columns = [col[0] for col in cursor.description]
        brands = [dict(zip(columns, row)) for row in cursor.fetchall()]

        query = '''
            SELECT p.*, s.quantity FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid  
            WHERE p.categoryid = %s
        '''
        params = [id]

        if brand_id:
            query += " AND p.brandid = %s"
            params.append(brand_id)

        if min_price and max_price:
            query += " AND COALESCE(p.discountedprice, p.baseprice) BETWEEN %s AND %s"
            params.extend([min_price, max_price])

        if stock_filter == 'in_stock':
            query += " AND s.quantity > 0"
        elif stock_filter == 'out_of_stock':
            query += " AND s.quantity = 0"

        if search_query:
            query += " AND (p.name ILIKE %s OR p.productserialnumber ILIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        if discount_filter == 'com_desconto':
            query += " AND p.discountedprice IS NOT NULL"
        elif discount_filter == 'sem_desconto':
            query += " AND p.discountedprice IS NULL"

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.execute("SELECT * FROM static_content.categories_with_instruments;")
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]


    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category_name': category_name,
        'categories': categories,
        'brands': brands,
        'selected_brand': brand_id, 
        'min_price': min_price,
        'max_price': max_price,
        'min_db_price': min_db_price,
        'max_db_price': max_db_price,
        'selected_stock': stock_filter,
        'search_query': search_query,
        'selected_discount': discount_filter 
    }
    return render(request, 'category_detail.html', context)


    with connection.cursor() as cursor:

        cursor.execute('''
            SELECT * FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid 
            WHERE p.categoryid = %s AND p."producttype" = \'accessories\'
        ''', [id])
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        

        cursor.execute('''
            SELECT name FROM static_content.categories c 
            WHERE categoryid = %s
        ''', [id])
        category_name = cursor.fetchone()
        
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."producttype" = \'accessories\');')
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
            SELECT p.*, s.*, 
                   COALESCE(b.brandname, 'Sem Marca') AS brandname
            FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid 
            LEFT JOIN dynamic_content.brands b ON b.brandid = p.brandid
            WHERE p.productid = %s
        ''', [id])
        
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            product = dict(zip(columns, row))
        else:
            product = None

        cursor.execute('SELECT * FROM static_content.categories')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    context = {'product': product, 'categories': categories}
    return render(request, 'product_detail.html', context)

def add_to_cart(request, id, stock):
    cart_cookie = request.COOKIES.get('cart', '{}')
    try:
        cart_cookie = cart_cookie.replace('\054', ',').replace('\\"', '"').strip('"')
        cart = json.loads(cart_cookie)
    except json.JSONDecodeError:
        cart = {}
    id = str(id)
    if id in cart:
        if stock > cart[id]:
            cart[id] += 1
            response = JsonResponse({'message': 'Produto adicionado ao carrinho', 'cart': cart})
        else:
            response = JsonResponse({'message': 'Produto não adicionado ao carrinho devido à falta de stock', 'cart': cart})
    else:
        if stock > 0:
            cart[id] = 1
            response = JsonResponse({'message': 'Produto adicionado ao carrinho', 'cart': cart})
        else:
            response = JsonResponse({'message': 'Produto não adicionado ao carrinho devido à falta de stock', 'cart': cart})
    cart_json = json.dumps(cart, separators=(',', ':'))
    response.set_cookie('cart', cart_json, path='/', max_age=31536000)
    return response

def admin(request):
    userID = request.session.get('user_id')

    if userID is None:
        return redirect('index')

    with connection.cursor() as cursor:
        cursor.execute("SELECT is_user_manager(%s);", [userID])
        isadmin = cursor.fetchone()

    if isadmin and isadmin[0]:
        return render(request, 'admin.html')
    else:
        return redirect('index')

def get_cart_items(request):
    product_ids = request.GET.get('ids', '')

    if not product_ids:
        return JsonResponse({"products": []})

    product_ids = urllib.parse.unquote(product_ids).replace('\\054', ',')
    product_ids = [id.strip('"') for id in product_ids.split(',') if id.strip('"').isdigit()]

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

def add_content(request, tablename):
    if request.method == 'POST':
        print(request.POST)

        if tablename == 'dynamic_content.stock':
            ProductID = request.POST.get('productid')
            quantity = request.POST.get('quantity')

            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE {tablename} SET quantity = quantity + %s, lastupdated = NOW() WHERE productid = %s", [quantity, ProductID])
                return redirect('admin')

        elif tablename == 'static_content.categories':
            name = request.POST.get('name')
            description = request.POST.get('description')
            preview_img = request.FILES.get('preview_img')

            preview_img_url = upload_to_cloudinary.upload_image(preview_img) if preview_img else None

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO static_content.categories (name, description, preview_img) VALUES (%s, %s, %s)",
                    [name, description, preview_img_url]
                )

            return redirect('admin')

        elif tablename == 'dynamic_content.products':
            name = request.POST.get('name')
            description = request.POST.get('description')
            baseprice = request.POST.get('baseprice')
            discountedprice = request.POST.get('discountedprice')
            brandid = request.POST.get('brandid')

            try:
                baseprice = float(baseprice) if baseprice else None
                discountedprice = float(discountedprice) if discountedprice else None
                brandid = float(brandid)
            except ValueError:
                baseprice = None
                discountedprice = None

            productserialnumber = request.POST.get('productserialnumber')
            producttype = request.POST.get('producttype')
            categoryid = request.POST.get('categoryid')

            try:
                categoryid = int(categoryid) if categoryid else None
            except ValueError:
                categoryid = None

            image_url = request.FILES.get('image_url')

            image_url = upload_to_cloudinary.upload_image(image_url) if image_url else None

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO dynamic_content.products (name, description, baseprice, discountedprice, productserialnumber, categoryid, producttype, image_url, brandid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    [name, description, baseprice, discountedprice, productserialnumber, categoryid, producttype, image_url, brandid]
                )

            return redirect('admin')

        elif tablename == 'dynamic_content.brands':
            brandname = request.POST.get('brandname')

            if not brandname:
                return HttpResponse("O nome da marca é obrigatório.", status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO dynamic_content.brands (brandname) VALUES (%s)",
                    [brandname]
                )

            return redirect('admin')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s
            AND ordinal_position > 1  -- Skip the first column (ID)
            ORDER BY ordinal_position
        """, [tablename.split('.')[-1]])

        fields = []
        for column in cursor.fetchall():
            fields.append({'name': column[0], 'type': column[1]})

        cursor.execute("SELECT * FROM static_content.categories")
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.execute("SELECT * FROM dynamic_content.products")
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM dynamic_content.brands")
        columns = [col[0] for col in cursor.description]
        brands = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'table_name': tablename,
        'fields': fields,
        'categories': categories,
        'products': products,
        'brands': brands
    }

    userID = request.session.get('user_id')

    if userID is None:
        return redirect('index')

    with connection.cursor() as cursor:
        cursor.execute("SELECT is_user_manager(%s);", [userID])
        isadmin = cursor.fetchone()

    if isadmin and isadmin[0]:
        return render(request, 'add_content.html', context)
    else:
        return redirect('index')

def adminview(request, tablename):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {tablename}")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        if(tablename != "static_content.categories"):
            cursor.execute("SELECT categoryid, name FROM static_content.categories")
            category_dict = {row[0]: row[1] for row in cursor.fetchall()}
            for item in data:
                if "categoryid" in item and item["categoryid"] in category_dict:
                    item["categoryid"] = category_dict[item["categoryid"]]

    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'table_name': tablename,
        'columns': columns,
        'page_obj': page_obj,
    }
    
    userID = request.session.get('user_id')

    if userID is None:
        return redirect('index')

    with connection.cursor() as cursor:
        cursor.execute("SELECT is_user_manager(%s);", [userID])
        isadmin = cursor.fetchone()

    if isadmin and isadmin[0]:
        return render(request, 'adminview.html', context)
    else:
        return redirect('index')
    
def delete_content(request, tablename, id):
    if request.method != "POST":
        return HttpResponse("Método inválido", status=400)

    try:
        primary_keys = {
            "dynamic_content.products": "productid",
            "static_content.categories": "categoryid",
            "dynamic_content.brands": "brandid"
        }
        
        primary_key = primary_keys.get(tablename)
        if not primary_key:
            return HttpResponse("Tabela inválida", status=400)


        userID = request.session.get('user_id')
        if userID is None:
            return redirect('index')

        with connection.cursor() as cursor:
            cursor.execute("SELECT is_user_manager(%s);", [userID])
            isadmin = cursor.fetchone()

        if not (isadmin and isadmin[0]):
            return redirect('index')

        with connection.cursor() as cursor:
            query = f"DELETE FROM {tablename} WHERE {primary_key} = %s"
            cursor.execute(query, [id])

        return redirect('adminview', tablename=tablename)

    except Exception as e:
        return HttpResponse(f"Erro ao excluir o item: {e}", status=500)

def edit_content(request, tablename, id):

    primary_keys = {
        "static_content.categories": "categoryid",
        "dynamic_content.products": "productid",
        "dynamic_content.brands": "brandid",
        "hr.users": "userid"
    }

    primary_key = primary_keys.get(tablename)
    if not primary_key:
        return HttpResponse("Tabela inválida", status=400)

 
    userID = request.session.get('user_id')
    if userID is None:
        return redirect('index')


    with connection.cursor() as cursor:
        cursor.execute("SELECT is_user_manager(%s);", [userID])
        is_manager = cursor.fetchone()

    if not (is_manager and is_manager[0]):
        return redirect('index')

    if request.method == "POST":
 
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tablename} WHERE {primary_key} = %s", [id])
            row = cursor.fetchone()
            if not row:
                return HttpResponse("Registro não encontrado", status=404)

            columns = [col[0] for col in cursor.description]
            existing_data = dict(zip(columns, row)) 

        update_columns = []
        update_values = []

        print("POST DATA:", request.POST.dict())  

        for col in columns:
            if col == primary_key:
                continue
            elif col in ["image_url", "preview_img"]:
                image_file = request.FILES.get(col) 

                if image_file: 
                    upload_result = upload_to_cloudinary.upload_image(image_file)
                    print("UPLOAD RESULT:", upload_result)

                    image_url = upload_result if upload_result else existing_data[col] 
                else:
                    image_url = existing_data[col]  

                update_columns.append(f"{col} = %s")
                update_values.append(image_url)

            else:
                value = request.POST.get(col, existing_data[col])
                if value in ["", None, "None"]: 
                    value = existing_data[col]
                update_columns.append(f"{col} = %s")
                update_values.append(value)

        update_values.append(id)

        update_query = f"UPDATE {tablename} SET {', '.join(update_columns)} WHERE {primary_key} = %s"
        
        print("QUERY:", update_query)
        print("VALUES:", update_values)

        with connection.cursor() as cursor:
            cursor.execute(update_query, update_values)
            connection.commit()

        return redirect('adminview', tablename=tablename)

    else:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tablename} WHERE {primary_key} = %s", [id])
            row = cursor.fetchone()
            if not row:
                return HttpResponse("Registro não encontrado", status=404)

            columns = [col[0] for col in cursor.description]
            data = dict(zip(columns, row))

        context = {
            'table_name': tablename,
            'data': data,
            'columns': columns,
        }
        return render(request, 'edit_content.html', context)

def get_product_info(request, product_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, image_url FROM dynamic_content.products WHERE productid = %s", [product_id])
        row = cursor.fetchone()
        if row:
            return JsonResponse({"name": row[0], "image_url": row[1]})
        else:
            return JsonResponse({"name": "Produto não encontrado", "image_url": "/static/images/not-found.png"}, status=404)