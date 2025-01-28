from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product_card", views.product_card, name="product_card"),
    path("top_bar", views.top_bar, name="top_bar"),
    path("navbar", views.navbar, name="navbar"),
    path("brand/<int:brand_id>/", views.brand, name="brand"),
    path("filter_card", views.filter_card, name="filter_card"),
    path("product_details", views.product_details, name="product_details"),
    path("brand_details", views.brand_details, name="brand_details"),
    path("base", views.base, name="base"),
    path("payment_details", views.payment_details, name="payment_details"),
    path("brands_page", views.brands_page, name="brands_page"),
    path("store", views.store, name="store"),
    path("instruments", views.instruments, name="instruments"), #URL da Navbar para Instrumentos
    path("new", views.new, name="new"), #URL da Navbar para novidades
    path("highlights", views.highlights, name="highlights"), #URL da Navbar para Destaques
    path("accessories", views.accessories, name="accessories"), #URL da Navbar para Acessórios
    path("discount", views.discount, name="discount"), #URL da Navbar para Descontos
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add_to_basket/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path("order_history", views.order_history, name="order_history"),
    path("logout", views.logout, name="logout"),
    path("checkout/<int:product_id>/", views.checkout, name="checkout"),
    path("cart", views.cart, name="cart"),
    path('category_detail/<int:id>/', views.category_detail, name='category_detail'),
    path('product_detail/<int:id>/', views.product_detail, name='product_detail'),
]
