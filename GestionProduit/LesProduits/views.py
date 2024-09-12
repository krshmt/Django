from django.shortcuts import render
from .models import Product

# Create your views here.


from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1> Bonjour, voici ma premiere vue </h1>")


def about(request):
    return HttpResponse("<h1> Bonjour, voici ma vue about </h1>")

def hello(request,name):
    return HttpResponse("<h1> Bonjour, " +name +" voici ma vue hello </h1>")


def comparer(request,nb1,nb2):
    if nb1>nb2:
        return HttpResponse("<h1> "+nb1 +" est plus grand que "+nb2 +"</h1>")
    else:
        return HttpResponse(nb2 +" est plus grand que "+nb1)

def ListProduct(request):
    products = Product.objects.all()
    rep = "<h1> Liste des produits </h1>"
    for product in products:
        rep += "<p>"+product.name +"</p>"
    return HttpResponse(rep)