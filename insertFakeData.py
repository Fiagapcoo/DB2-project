import os
import django
import random
from datetime import date, timedelta
from faker import Faker

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import models
from store.models import Clientes, Fornecedores, Categoria, Produtos, Stock, Promocoes, Colaboradores, Pedido, Pagamentos, ComprasForn

# Faker instance for generating fake data
fake = Faker()

# Generate fake data for each model

def insert_fake_data():
    # Insert fake Clientes
    for _ in range(10):
        Clientes.objects.create(
            nome=fake.name(),
            telefone=fake.phone_number()[:20],  # Truncate phone number to 20 chars
            morada=fake.address(),
            email=fake.email(),
            nif=fake.unique.numerify(text='##########')[:20]  # Truncate NIF to 20 chars
        )
    
    # Insert fake Fornecedores
    for _ in range(5):
        Fornecedores.objects.create(
            nome_forn=fake.company(),
            email_form=fake.company_email(),
            telefone_forn=fake.phone_number()[:20],  # Truncate phone number to 20 chars
            nifc_forn=fake.unique.numerify(text='##########')[:20]  # Truncate NIFC to 20 chars
        )

    # Insert fake Categoria
    categories = []
    for _ in range(3):
        category = Categoria.objects.create(
            nome_cat=fake.word(),
            desc_cat=fake.text(max_nb_chars=100)
        )
        categories.append(category)

    # Insert fake Produtos
    forns = Fornecedores.objects.all()
    for _ in range(20):
        produto = Produtos.objects.create(
            nome_produto=fake.word(),
            preco=random.uniform(10, 500),
            descricao=fake.text(),
            stock=random.randint(1, 100),
            marca=fake.company()[:100],  # Truncate brand name to 100 chars
            id_fornecedor=random.choice(forns),
            id_categoria=random.choice(categories),
            sn_produto=fake.unique.numerify(text='SN-#######')[:100]  # Truncate serial number to 100 chars
        )
        # Insert corresponding Stock
        Stock.objects.create(
            id_produto=produto,
            quantidade_disponivel=random.randint(10, 100),
            quantidade_reservada=random.randint(0, 50)
        )

    # Insert fake Promocoes
    produtos = Produtos.objects.all()
    for _ in range(5):
        promocao = Promocoes.objects.create(
            valor_desconto=random.uniform(5, 50),
            inicio_desc=date.today(),
            fim_desc=date.today() + timedelta(days=random.randint(1, 30))
        )
        promocao.produtos.set(random.sample(list(produtos), random.randint(1, 5)))

    # Insert fake Colaboradores
    for _ in range(5):
        Colaboradores.objects.create(
            nome_colaborador=fake.name(),
            email=fake.email(),
            passwd=fake.password(),
            telefone=fake.phone_number()[:20],  # Truncate phone number to 20 chars
            cargo=fake.job()[:100]  # Truncate job title to 100 chars
        )

    # Insert fake Pedido and related Pagamentos
    clientes = Clientes.objects.all()
    colaboradores = Colaboradores.objects.all()
    for _ in range(10):
        pedido = Pedido.objects.create(
            id_cliente=random.choice(clientes),
            id_colaborador=random.choice(colaboradores),
            valor_total=random.uniform(100, 1000),
            estado_pedido=fake.word(),
            pedido_json_form={"items": fake.words(nb=3)}
        )
        # Insert corresponding Pagamento
        Pagamentos.objects.create(
            metodo_pagamento=random.choice(['Credit Card', 'PayPal', 'Bank Transfer'])[:50],  # Truncate payment method to 50 chars
            valor_pago=pedido.valor_total,
            id_pedido=pedido,
            estado_pagamento=random.choice(['Completed', 'Pending', 'Failed'])[:50]  # Truncate payment status to 50 chars
        )

    # Insert fake ComprasForn
    forns = Fornecedores.objects.all()
    for _ in range(5):
        ComprasForn.objects.create(
            id_forn=random.choice(forns),
            compra_json_form={"products": fake.words(nb=3)},
            valor_total_compra=random.uniform(500, 2000),
            estado_compra=random.choice(['Completed', 'Pending', 'Cancelled'])[:50]  # Truncate purchase status to 50 chars
        )

    print("Fake data inserted successfully!")

if __name__ == "__main__":
    insert_fake_data()
