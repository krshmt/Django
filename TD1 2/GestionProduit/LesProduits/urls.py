from django.urls import path
from . import views
from django.views.generic import *
from .views import *
from django.urls import path
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),
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
    #path("product/add/",views.ProductCreate, name="product-add"),
    path("product/add/",views.ProductCreateView.as_view(), name="product-add"),
    path("product/<pk>/update/",views.ProductUpdateView.as_view(), name="product-update"),
    path("product/<pk>/delete/",views.ProductDeleteView.as_view(), name="product-delete"),
    path('attributes/', views.ProductAttributeListView.as_view(), name='attribute-list'),
    path('attribute/<int:pk>/', views.ProductAttributeDetailView.as_view(), name='attribute-detail'),
    path('item/', views.ProductItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', views.ProductItemDetailView.as_view(), name='detail_item'),
    path('product/<int:product_id>/commander/', views.commander_produit, name='commande-produit'),
    path('commandes/', views.CommandeListView.as_view(), name='commande-list'),
    path('commandes/<int:pk>/', views.CommandeDetailView.as_view(), name='commande-detail'),
    path('commandes/ajouter/', views.CommandeCreateView.as_view(), name='commande-create'),
    path('commandes/<int:pk>/modifier/', views.CommandeUpdateView.as_view(), name='commande-update'),
    path('commandes/<int:pk>/supprimer/', views.CommandeDeleteView.as_view(), name='commande-delete'),
    path('fournisseurs/', FournisseurListView.as_view(), name='fournisseur-list'),
    path('fournisseur/<int:pk>/', FournisseurDetailView.as_view(), name='fournisseur-detail'),
    path('fournisseur/new/', FournisseurCreateView.as_view(), name='fournisseur-create'),
    path('fournisseur/<int:pk>/edit/', FournisseurUpdateView.as_view(), name='fournisseur-update'),
    path('fournisseur/<int:pk>/delete/', FournisseurDeleteView.as_view(), name='fournisseur-delete'),
]

