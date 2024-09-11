from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("about", views.about, name='about'),
    path("hello/<name>", views.hello, name='hello'),
    path("comparer/<nb1>/<nb2>", views.comparer, name='comparer'),
]

