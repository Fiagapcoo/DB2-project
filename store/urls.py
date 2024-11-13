from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product_card", views.product_card, name="product_card"),
    path("top_bar", views.top_bar, name="top_bar"),
    path("navbar", views.navbar, name="navbar"),
    path("brand", views.brand, name="brand"),
    path("filter_card", views.filter_card, name="filter_card"),
    path("product_details", views.product_details, name="product_details"),
    path("brand_details", views.brand_details, name="brand_details"),
    path("base", views.base, name="base"),
]
