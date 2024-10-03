from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from LesProduits.models import Product, ProductAttribute, ProductAttributeValue, ProductItem
from LesProduits.form import ContactUsForm, ProductForm
from django.views.generic import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

# Create your views here.


from django.http import HttpResponse

def index(request):
    name = request.GET.get("name")
    if name is None:
        name = "inconnu"
    return HttpResponse("<h1> Bonjour " + name + " voici ma premiere vue </h1>")

def home(request):
    return HttpResponse("<h1> Bonjour, voici ma vue home </h1>")

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
    return render(request, 'listProducts.html', {'products': products}) 

class HomeView(TemplateView):
    template_name = "home.html"
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO"
        return context


class AboutView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "A propos de nous"
        return context
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
class ProductListView(ListView):
    model = Product
    template_name = "listProducts.html"
    context_object_name = "products"

class ProductDetailView(DetailView):
    model = Product
    template_name = "detail_product.html"
    context_object_name = "product"
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit"
        return context
    

class ConnectView(LoginView):
    template_name = 'login.html'
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'hello.html',{'titreh1':"hello "+username+", you're connected"})
        else:
            return render(request, 'register.html')
    
def ContactView(request):
    titreh1 = "Contact us !"
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@monprojet.com'],
            )
            return redirect('email-sent')
    else:
        form = ContactUsForm()
        return render(request, "contact.html",{'titreh1':titreh1, 'form':form})
            
class RegisterView(TemplateView):
    template_name = 'register.html'
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'login.html')
        else:
            return render(request, 'register.html')
        
class DisconnectView(TemplateView):
    template_name = 'logout.html'
    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    
###################################################################################################################################################

class ProductCreateView(CreateView):
    model = Product
    form_class=ProductForm
    template_name = "new_product.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)
    
class ProductUpdateView(UpdateView):
    model = Product
    form_class=ProductForm
    template_name = "update_product.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)
    
def ProductUpdate(request, id):
    prdct = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=prdct)
        if form.is_valid():
            # mettre à jour le produit existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du produit que nous venons de mettre à jour
            return redirect('product-detail', prdct.id)
    else:
        form = ProductForm(instance=prdct)
    return render(request,'product-update.html', {'form': form}) 

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product_delete.html"
    success_url = reverse_lazy('product-list')



class ProductAttributeListView(ListView):
    model = ProductAttribute
    template_name = "list_attributes.html"
    context_object_name = "productattributes"
    def get_queryset(self ):
        return ProductAttribute.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(ProductAttributeListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des attributs"
        return context
    
class ProductAttributeDetailView(DetailView):
    model = ProductAttribute
    template_name = "detail_attribute.html"
    context_object_name = "productattribute"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail attribut"
        context['values']=ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position')
        return context
    
class ProductItemListView(ListView):
    model = ProductItem
    template_name = "list_items.html"
    context_object_name = "productitems"
    def get_queryset(self ):
        return ProductItem.objects.all()
    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des déclinaisons"
        return context
    
class ProductItemDetailView(DetailView):
    model = ProductItem
    template_name = "detail_item.html"
    context_object_name = "productitem"
    def get_context_data(self, **kwargs):
        context = super(ProductItemDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail déclinaison"
        # Récupérer les attributs associés à cette déclinaison
        context['attributes'] = self.object.attributes.all()
        return context