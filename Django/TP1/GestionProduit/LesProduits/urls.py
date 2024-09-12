from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("about", views.about, name='about'),
    path("hello/<name>", views.hello, name='hello'),
    path("comparer/<nb1>/<nb2>", views.comparer, name='comparer'),
<<<<<<< HEAD:TP1/GestionProduit/LesProduits/urls.py
    path("ListProduct", views.ListProduct, name='ListProduct'),
=======
    path("ListeProduits", views.ListeProduits, name='ListeProduits'),
>>>>>>> aa98604 (pour kris):GestionProduit/LesProduits/urls.py
]

