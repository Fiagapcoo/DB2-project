from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Clientes)
admin.site.register(Fornecedores)
admin.site.register(Categoria)
admin.site.register(Produtos)
admin.site.register(Stock)
admin.site.register(Promocoes)
admin.site.register(Colaboradores)
admin.site.register(Pedido)
admin.site.register(Pagamentos)
admin.site.register(ComprasForn)