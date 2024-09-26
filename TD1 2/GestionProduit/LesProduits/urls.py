from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path("hello/<name>", views.hello, name='hello'),
    path("comparer/<nb1>/<nb2>", views.comparer, name='comparer'),
    path("ListeProduits", views.ListeProduits, name='ListeProduits'),
    path("productsview", views.lesProduits, name='productsview'),
    path("home", views.HomeView.as_view()),
    path('about/', views.AboutView.as_view()),
    path("product/list",views.ProductListView.as_view(), name="product-list"),
    path("product/<pk>" ,views.ProductDetailView.as_view(), name="product-detail"),
    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    path('contact/', views.ContactView, name='contact'),
]

