from django.db import models

class Clientes(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    morada = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    nif = models.CharField(max_length=20, unique=True, blank=True, null=True)
    data_registo = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Fornecedores(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    nome_forn = models.CharField(max_length=255)
    email_form = models.EmailField(max_length=255, unique=True)
    telefone_forn = models.CharField(max_length=20, blank=True, null=True)
    nifc_forn = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return self.nome_forn

class Categoria(models.Model):
    id_cat = models.AutoField(primary_key=True)
    nome_cat = models.CharField(max_length=100)
    desc_cat = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_cat

class Produtos(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    stock = models.IntegerField()
    foto_produto = models.TextField(blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    id_fornecedor = models.ForeignKey(Fornecedores, on_delete=models.CASCADE, null=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    sn_produto = models.CharField(max_length=100, unique=True, blank=True, null=True)
    # Removed id_promocao to avoid circular reference

    def __str__(self):
        return self.nome_produto

class Stock(models.Model):
    id_produto = models.OneToOneField(Produtos, on_delete=models.CASCADE, primary_key=True, related_name='produto_stock')
    quantidade_disponivel = models.IntegerField()
    quantidade_reservada = models.IntegerField(blank=True, null=True)
    data_ultima_atualizacao = models.DateField(auto_now=True)

    def __str__(self):
        return f"Stock for {self.id_produto.nome_produto}"

class Promocoes(models.Model):
    id_promocao = models.AutoField(primary_key=True)
    produtos = models.ManyToManyField(Produtos, related_name='promocoes', blank=True)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2)
    inicio_desc = models.DateField()
    fim_desc = models.DateField()

    def __str__(self):
        return f"Promotion {self.id_promocao}"

class Colaboradores(models.Model):
    id_colaborador = models.AutoField(primary_key=True)
    nome_colaborador = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    passwd = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome_colaborador

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    data_pedido = models.DateField(auto_now_add=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_colaborador = models.ForeignKey(Colaboradores, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado_pedido = models.CharField(max_length=50, blank=True, null=True)
    pedido_json_form = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Pedido {self.id_pedido}"

class Pagamentos(models.Model):
    id_pagamento = models.AutoField(primary_key=True)
    metodo_pagamento = models.CharField(max_length=50)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    data_pagamento = models.DateField(auto_now_add=True)
    estado_pagamento = models.CharField(max_length=50)

    def __str__(self):
        return f"Pagamento {self.id_pagamento}"

class ComprasForn(models.Model):
    id_compra = models.AutoField(primary_key=True)
    id_forn = models.ForeignKey(Fornecedores, on_delete=models.CASCADE)
    compra_json_form = models.JSONField(blank=True, null=True)
    valor_total_compra = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateField(auto_now_add=True)
    estado_compra = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Compra {self.id_compra}"
    
class Product(models.Model):
    
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    image_url = models.URLField()
    colors = models.JSONField(default=list)
    sizes = models.JSONField(default=list)

    def __str__(self):
        return self.name
