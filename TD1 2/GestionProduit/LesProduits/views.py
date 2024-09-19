from django.shortcuts import render
from LesProduits.models import Product

# Create your views here.


from django.http import HttpResponse

def index(request):
    name = request.GET.get("name")
    if name is None:
        name = "inconnu"
    return HttpResponse("<h1> Bonjour " + name + " voici ma premiere vue </h1>")


def about(request):
    return HttpResponse("<h1> Bonjour, voici ma vue about </h1>")

def hello(name):
    return HttpResponse("<h1> Bonjour, " +name +" voici ma vue hello </h1>")


def comparer(request,nb1,nb2):
    if nb1>nb2:
        return HttpResponse("<h1> "+nb1 +" est plus grand que "+nb2 +"</h1>")
    else:
        return HttpResponse(nb2 +" est plus grand que "+nb1)


def ListeProduits(request):
    products = Product.objects.all()
    print(products)
    rep = "<h1> Liste des produits </h1><ul>"
    for product in products:
        rep += "<li>"+product.name+"</li>"
    rep += "</ul>"
    return HttpResponse(rep)


def lesProduits(request):
    products = Product.objects.all()
    print(products)
    return render(request, 'LesProduits/listProducts.html', {'products': products}) 
    