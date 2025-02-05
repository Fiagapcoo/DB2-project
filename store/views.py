from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import *
from django.core.paginator import Paginator
from django.db import connection
from .mock_data import PRODUCTS
from django.http import JsonResponse
import urllib.parse
from . import upload_to_cloudinary
import json

def example_view(request):
    """A sample view function that will be logged."""
    return JsonResponse({"message": "This view was logged to MongoDB!"})

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
        # Fetch instruments
        cursor.execute('''
            SELECT * FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid  
            WHERE p.producttype = 'instrument'
        ''')
        columns = [col[0] for col in cursor.description]
        instruments = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Fetch categories
        cursor.execute('''
            SELECT * FROM static_content.categories c 
            WHERE EXISTS (
                SELECT 1 FROM dynamic_content.products p 
                WHERE p.categoryid = c.categoryid 
                AND p.producttype = 'instrument'
            );
        ''')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Pagination
    paginator = Paginator(instruments, 15)  # 15 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Pass paginated data
        'categories': categories
    }
    return render(request, 'instruments.html', context)

def store(request):
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

def top_bar(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."producttype" = \'instrument\');')
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
        cursor.execute('SELECT * FROM static_content.categories c WHERE EXISTS ( SELECT 1 FROM dynamic_content.products p WHERE p.categoryid = c.categoryid AND p."producttype" = \'accessories\';')
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
    categorias = Categoria.objects.all()
    return render(request, 'filter_card.html', {'categorias': categorias})

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
    category_id = request.GET.get('categoria', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    stock_filter = request.GET.get('stock', '')
    search_query = request.GET.get('search', '')

    with connection.cursor() as cursor:
        # Buscar categorias
        cursor.execute("SELECT * FROM static_content.categories")
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Buscar faixa de preço disponível
        cursor.execute("SELECT MIN(discountedprice), MAX(discountedprice) FROM dynamic_content.products WHERE discountedprice IS NOT NULL")
        min_db_price, max_db_price = cursor.fetchone()

        if not min_price:
            min_price = min_db_price
        if not max_price:
            max_price = max_db_price

        # Construir a query base
        query = '''
            SELECT p.*, s.quantity FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid  
            WHERE p.discountedprice IS NOT NULL
        '''
        params = []

        # Filtro de categoria
        if category_id:
            query += " AND p.categoryid = %s"
            params.append(category_id)

        # Filtro de preço
        if min_price and max_price:
            query += " AND p.discountedprice BETWEEN %s AND %s"
            params.extend([min_price, max_price])

        # Filtro de estoque
        if stock_filter == 'in_stock':
            query += " AND s.quantity > 0"
        elif stock_filter == 'out_of_stock':
            query += " AND s.quantity = 0"

        # Filtro de pesquisa
        if search_query:
            query += " AND (p.name ILIKE %s OR p.productserialnumber ILIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        # Ordenar pelos últimos 20 produtos adicionados
        query += " ORDER BY p.productid DESC LIMIT 20"

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Paginação
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'min_db_price': min_db_price,
        'max_db_price': max_db_price,
        'selected_stock': stock_filter,
        'search_query': search_query  # Passa a pesquisa para o template
    }
    return render(request, 'new.html', context)

def accessories(request):
    page_number = request.GET.get('page')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    stock_filter = request.GET.get('stock', '')
    search_query = request.GET.get('search', '')

    with connection.cursor() as cursor:
        # Buscar faixa de preço disponível para acessórios
        cursor.execute('''
            SELECT MIN(discountedprice), MAX(discountedprice)
            FROM dynamic_content.products
            WHERE producttype = 'accessories' AND discountedprice IS NOT NULL
        ''')
        min_db_price, max_db_price = cursor.fetchone()

        # Se os filtros de preço não estiverem preenchidos, usar os valores mínimos e máximos do BD
        if not min_price:
            min_price = min_db_price
        if not max_price:
            max_price = max_db_price

        # Construindo a query de produtos
        query = '''
            SELECT p.*, s.quantity FROM dynamic_content.products p
            JOIN dynamic_content.stock s ON s.productid = p.productid
            WHERE p.producttype = 'accessories'
        '''
        params = []

        # Aplicando filtro de preço
        if min_price and max_price:
            query += " AND p.discountedprice BETWEEN %s AND %s"
            params.extend([min_price, max_price])

        # Aplicando filtro de estoque
        if stock_filter == 'in_stock':
            query += " AND s.quantity > 0"
        elif stock_filter == 'out_of_stock':
            query += " AND s.quantity = 0"

        # Aplicando filtro de pesquisa (por nome ou número de série)
        if search_query:
            query += " AND (p.name ILIKE %s OR p.productserialnumber ILIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        accessories = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Buscar categorias relacionadas aos acessórios (Removemos pois a categoria não deve aparecer no filtro)
        cursor.execute('''
            SELECT * FROM static_content.categories c
            WHERE EXISTS (
                SELECT 1 FROM dynamic_content.products p
                WHERE p.categoryid = c.categoryid AND p.producttype = 'accessories'
            )
        ''')
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Aplicando paginação - 15 produtos por página
    paginator = Paginator(accessories, 15)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'min_price': min_price,
        'max_price': max_price,
        'min_db_price': min_db_price,
        'max_db_price': max_db_price,
        'selected_stock': stock_filter,
        'search_query': search_query,  # Adicionando pesquisa ao contexto
    }
    return render(request, 'accessories.html', context)

def discount(request):
    category_id = request.GET.get('categoria', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    stock_filter = request.GET.get('stock', '')
    search_query = request.GET.get('search', '')

    with connection.cursor() as cursor:
        # Buscar categorias
        cursor.execute("SELECT * FROM static_content.categories")
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Buscar faixa de preço disponível
        cursor.execute("SELECT MIN(discountedprice), MAX(discountedprice) FROM dynamic_content.products WHERE discountedprice IS NOT NULL")
        min_db_price, max_db_price = cursor.fetchone()

        if not min_price:
            min_price = min_db_price
        if not max_price:
            max_price = max_db_price

        # Construir a query base
        query = '''
            SELECT p.*, s.quantity FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid  
            WHERE p.discountedprice IS NOT NULL
        '''
        params = []

        # Filtro de categoria
        if category_id:
            query += " AND p.categoryid = %s"
            params.append(category_id)

        # Filtro de preço
        if min_price and max_price:
            query += " AND p.discountedprice BETWEEN %s AND %s"
            params.extend([min_price, max_price])

        # Filtro de estoque
        if stock_filter == 'in_stock':
            query += " AND s.quantity > 0"
        elif stock_filter == 'out_of_stock':
            query += " AND s.quantity = 0"

        # Filtro de pesquisa (nome ou número de série)
        if search_query:
            query += " AND (p.name ILIKE %s OR p.productserialnumber ILIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        produtos = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Paginação
    paginator = Paginator(produtos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'min_db_price': min_db_price,
        'max_db_price': max_db_price,
        'selected_stock': stock_filter,
        'search_query': search_query  # Passa a pesquisa para o template
    }
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

def order_details(request, order_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM transactions.orders WHERE orderid = %s", [order_id])
        order = cursor.fetchone()

        cursor.execute("SELECT paymentmethod, amount FROM transactions.payments WHERE orderid = %s", [order_id])
        payment = cursor.fetchone()

    if order:
        try:
            # Verifica se order[4] já é um dicionário
            items_data = order[4]
            if isinstance(items_data, str):  
                items_data = json.loads(items_data)  # Converte apenas se for string
            
            order_data = {
                "id": order[0],
                "transaction_code": order[2],
                "status": order[3],
                "items": items_data["items"],
                "payment_method": payment[0] if payment else "Desconhecido",
                "amount": payment[1] if payment else "0.00"
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
 

def category_detail(request, id):
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    stock_filter = request.GET.get('stock', '')
    search_query = request.GET.get('search', '')

    with connection.cursor() as cursor:
        # Buscar nome da categoria
        cursor.execute("SELECT name FROM static_content.categories WHERE categoryid = %s", [id])
        category_name = cursor.fetchone()

        if category_name:
            category_name = category_name[0]
        else:
            category_name = "Categoria Desconhecida"

        # Buscar a faixa de preço disponível nesta categoria
        cursor.execute('''
            SELECT MIN(discountedprice), MAX(discountedprice) 
            FROM dynamic_content.products 
            WHERE categoryid = %s AND discountedprice IS NOT NULL
        ''', [id])
        min_db_price, max_db_price = cursor.fetchone()

        if not min_price:
            min_price = min_db_price
        if not max_price:
            max_price = max_db_price

        # Construir a query base para produtos desta categoria
        query = '''
            SELECT p.*, s.quantity FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid  
            WHERE p.categoryid = %s
        '''
        params = [id]

        # Aplicar filtro de preço
        if min_price and max_price:
            query += " AND p.discountedprice BETWEEN %s AND %s"
            params.extend([min_price, max_price])

        # Aplicar filtro de estoque
        if stock_filter == 'in_stock':
            query += " AND s.quantity > 0"
        elif stock_filter == 'out_of_stock':
            query += " AND s.quantity = 0"

        # Aplicar filtro de pesquisa (nome ou número de série)
        if search_query:
            query += " AND (p.name ILIKE %s OR p.productserialnumber ILIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Buscar todas as categorias (para a barra de topo)
        cursor.execute("SELECT * FROM static_content.categories")
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Paginação - 15 produtos por página
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category_name': category_name,
        'categories': categories,
        'min_price': min_price,
        'max_price': max_price,
        'min_db_price': min_db_price,
        'max_db_price': max_db_price,
        'selected_stock': stock_filter,
        'search_query': search_query  # Passar a pesquisa para o template
    }
    return render(request, 'category_detail.html', context)

def category_detail_discount(request, id):
    # 🔹 Buscar os produtos da categoria com desconto
    products = Produtos.objects.filter(id_categoria=id, preco__isnull=False).select_related('id_categoria')

    # 🔹 Buscar o nome da categoria
    category = Categoria.objects.filter(id_cat=id).first()

    # 🔹 Aplicar paginação (15 produtos por página)
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,  # Passa apenas os produtos da página atual
        'category_name': category.nome_cat if category else 'Categoria Não Encontrada',
    }
    return render(request, 'category_detail_discount.html', context)

def category_detail_accessories(request, id):
    with connection.cursor() as cursor:
        # Get products with stock information
        cursor.execute('''
            SELECT * FROM dynamic_content.products p 
            JOIN dynamic_content.stock s ON s.productid = p.productid 
            WHERE p.categoryid = %s AND p."producttype" = \'accessories\'
        ''', [id])
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Get category name
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
    return render(request, 'admin.html')


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

def add_content(request, tablename):
    #TODO check if manager = true
    
    if request.method == 'POST':
        print(request.POST)
        if(tablename == 'dynamic_content.stock'):
            ProductID = request.POST.get('productid')
            quantity = request.POST.get('quantity')
            
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE {tablename} SET quantity = quantity + %s, lastupdated = NOW() WHERE productid = %s", [quantity, ProductID])
                return redirect('admin')
        elif tablename == 'static_content.categories':
            name = request.POST.get('name')
            description = request.POST.get('description')
            preview_img = request.FILES.get('preview_img')

            if preview_img:
                preview_img_url = upload_to_cloudinary.upload_image(preview_img) 
            else:
                preview_img_url = None 

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

            try:
                baseprice = float(baseprice) if baseprice else None
                discountedprice = float(discountedprice) if discountedprice else None
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

            if image_url:
                image_url = upload_to_cloudinary.upload_image(image_url) 
            else:
                image_url = None 

            print("INSERT COMMAND: INSERT INTO dynamic_content.products (name, description, baseprice, discountedprice, productserialnumber, categoryid, producttype, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                % (name, description, baseprice, discountedprice, productserialnumber, categoryid, producttype, image_url))

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO dynamic_content.products (name, description, baseprice, discountedprice, productserialnumber, categoryid, producttype, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    [name, description, baseprice, discountedprice, productserialnumber, categoryid, producttype, image_url]
                )

            return redirect('admin')

            
    
    # GET request handling (showing the form)
    with connection.cursor() as cursor:
        # First query: Get fields
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s
            AND ordinal_position > 1  -- Skip the first column (ID)
            ORDER BY ordinal_position
        """, [tablename.split('.')[-1]])
        
        fields = []
        for column in cursor.fetchall():
            fields.append({
                'name': column[0],
                'type': column[1]
            })
        
        # Second query: Get categories
        cursor.execute("SELECT * FROM static_content.categories")
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.execute(f"SELECT * FROM dynamic_content.products")
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'table_name': tablename,
        'fields': fields,
        'categories': categories,
        'products':products
    }
    
    print(context)
    
    return render(request, 'add_content.html', context)


def adminview(request, tablename):
    with connection.cursor() as cursor:
        # Fetch all data from the given table
        cursor.execute(f"SELECT * FROM {tablename}")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        # Fetch category names and replace the categoryid value if needed
        if(tablename != "static_content.categories"):
            cursor.execute("SELECT categoryid, name FROM static_content.categories")
            category_dict = {row[0]: row[1] for row in cursor.fetchall()}
            for item in data:
                if "categoryid" in item and item["categoryid"] in category_dict:
                    item["categoryid"] = category_dict[item["categoryid"]]

    # Paginate (20 rows per page)
    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'table_name': tablename,
        'columns': columns,
        'page_obj': page_obj,
    }
    
    print("context:   ", context)
    
    return render(request, 'adminview.html', context)

def delete_content(request, tablename, id):
    
    with connection.cursor() as cursor:
        # Call the stored procedure with parameter placeholders.
        cursor.execute("CALL delete_content(%s, %s)", [tablename, id])
    
    return redirect('adminview', tablename=tablename)


def edit_content(request, tablename, id):
    if tablename == "static_content.categories":
        primary_key = "categoryid"
    elif tablename == "dynamic_content.products":
        primary_key = "productid"
    else:
        return HttpResponse("Invalid table", status=400)

    if request.method == "POST":
        # Fetch the existing record
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tablename} WHERE {primary_key} = %s", [id])
            row = cursor.fetchone()
            if not row:
                return HttpResponse("Record not found", status=404)
            columns = [col[0] for col in cursor.description]
            existing_data = dict(zip(columns, row))  # Store existing values

        # Build the UPDATE query dynamically, excluding the primary key
        update_columns = []
        update_values = []

        for col in columns:
            if col == primary_key:  # Skip the primary key
                continue
            elif col in ["image_url", "preview_img"]:  # Handle image upload
                if request.FILES.get(col):  # If user uploaded a new image
                    upload_result = upload_to_cloudinary.upload_image(request.FILES[col])
                    image_url = upload_result["secure_url"]  # Get the Cloudinary URL
                else:
                    image_url = existing_data[col]  # Keep the old image if not updated

                update_columns.append(f"{col} = %s")
                update_values.append(image_url)
            else:
                update_columns.append(f"{col} = %s")
                update_values.append(request.POST.get(col, existing_data[col]))  # Keep old value if not changed

        update_values.append(id)  # Add the primary key value for WHERE clause

        update_query = f"UPDATE {tablename} SET {', '.join(update_columns)} WHERE {primary_key} = %s"

        with connection.cursor() as cursor:
            cursor.execute(update_query, update_values)

        return redirect('adminview', tablename=tablename)

    else:
        # GET request: fetch the existing record for editing
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tablename} WHERE {primary_key} = %s", [id])
            row = cursor.fetchone()
            if not row:
                return HttpResponse("Record not found", status=404)
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