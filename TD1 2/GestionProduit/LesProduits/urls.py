from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    path('', views.index, name='index'),
    path("hello/<name>", views.hello, name='hello'),
    path("comparer/<nb1>/<nb2>", views.comparer, name='comparer'),
    path("ListeProduits", views.ListeProduits, name='ListeProduits'),
    path("productsview", views.lesProduits, name='productsview'),
    path("home", views.HomeView.as_view()),
    path('about/', views.AboutView.as_view()),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path("product/list",views.ProductListView.as_view()),
    path("product/<pk>" ,views.ProductDetailView.as_view(), name="product-detail"),
]

