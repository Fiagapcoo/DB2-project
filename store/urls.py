from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product_card", views.product_card, name="product_card"),
    path("top_bar", views.top_bar, name="top_bar"),
    path("navbar", views.navbar, name="navbar"),
    path("filter_card", views.filter_card, name="filter_card"),
    path("base", views.base, name="base"),
    path("payment_details", views.payment_details, name="payment_details"),
    path("store", views.store, name="store"),
    path("instruments", views.instruments, name="instruments"),
    path("new", views.new, name="new"), 
    path("accessories", views.accessories, name="accessories"), 
    path("discount", views.discount, name="discount"),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path("order_history", views.order_history, name="order_history"),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),
    path("logout", views.logout, name="logout"),
    path("checkout/<int:product_id>/", views.checkout, name="checkout"),
    path("cart", views.cart, name="cart"),
    path('add-to-cart/<int:id>/<int:stock>/', views.add_to_cart, name='add_to_cart'),
    path('category_detail/<int:id>/', views.category_detail, name='category_detail'),
    path('product_detail/<int:id>/', views.product_detail, name='product_detail'),
    path('get-cart-items/', views.get_cart_items, name='get_cart_items'),
    path('get-product-info/<int:product_id>/', views.get_product_info, name='get_product_info'),
    path("process-checkout/", views.process_checkout, name="process_checkout"),

    
    
    ##ADMIN URLS
    
    path('adminpage/', views.admin, name='admin'),
    path('add_content/<str:tablename>/', views.add_content, name='add_content'),
    path('adminview/<str:tablename>/', views.adminview, name='adminview'),
    path('delete_content/<str:tablename>/delete/<int:id>/', views.delete_content, name='delete_content'),
    path('edit_content/<str:tablename>/edit/<int:id>/', views.edit_content, name='edit_content'),
]
