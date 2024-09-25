from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    path('', views.index, name='index'),
    path("about", views.about, name='about'),
    path("hello/<name>", views.hello, name='hello'),
    path("comparer/<nb1>/<nb2>", views.comparer, name='comparer'),
    path("ListeProduits", views.ListeProduits, name='ListeProduits'),
    path("productsview", views.lesProduits, name='productsview'),
    path("home", TemplateView.as_view(template_name="home.html")),
]

