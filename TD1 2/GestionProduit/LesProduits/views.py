from datetime import timezone
from django.contrib import messages
from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from LesProduits.models import Product, ProductAttribute, ProductAttributeValue, ProductItem, Fournisseur, Commande, CommandeProduit
from LesProduits.forms import ContactUsForm, ProductForm, FournisseurForm, CommandeForm, CommandeProduitForm
from django.views.generic import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.db import transaction
from .forms import CommandeForm, CommandeProduitFormSet
from django.utils import timezone
from .models import Fournisseur
from .forms import FournisseurForm
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin

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
    
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "listProducts.html"
    context_object_name = "products"
    login_url = '/login/'
    
    def get_queryset(self ):

        query = self.request.GET.get('search')
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des produits"
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "detail_product.html"
    context_object_name = "product"
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit"
        return context
    

class ConnectView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('product-list')

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(self.get_success_url())
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
            
class RegisterView(LoginRequiredMixin, TemplateView):
    template_name = 'register.html'
    login_url = '/login/'
    
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
        
class DisconnectView(LoginRequiredMixin, TemplateView):
    template_name = 'logout.html'
    login_url = '/login/'
    
    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    
###################################################################################################################################################

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class=ProductForm
    template_name = "new_product.html"
    login_url = '/login/'
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)
    
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class=ProductForm
    template_name = "update_product.html"
    login_url = '/login/'
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)
    
    def ProductUpdate(request, id):
        prdct = Product.objects.get(id=id)
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=prdct)
            if form.is_valid():
                form.save()
                return redirect('product-detail', prdct.id)
        else:
            form = ProductForm(instance=prdct)
        return render(request,'product-update.html', {'form': form}) 

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_delete.html"
    success_url = reverse_lazy('product-list')
    login_url = '/login/'


class ProductAttributeListView(LoginRequiredMixin, ListView):
    model = ProductAttribute
    template_name = "list_attributes.html"
    context_object_name = "productattributes"
    login_url = '/login/'
    
    def get_queryset(self ):
        return ProductAttribute.objects.all().prefetch_related('productattributevalue_set')
    def get_context_data(self, **kwargs):
        context = super(ProductAttributeListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des attributs"
        return context
    
class ProductAttributeDetailView(LoginRequiredMixin, DetailView):
    model = ProductAttribute
    template_name = "detail_attribute.html"
    context_object_name = "productattribute"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail attribut"
        context['values']=ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position')
        return context
    
class ProductItemListView(LoginRequiredMixin, ListView):
    model = ProductItem
    template_name = "list_items.html"
    context_object_name = "productitems"
    login_url = '/login/'
    
    def get_queryset(self):
        return ProductItem.objects.select_related('product').prefetch_related('attributes')
    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des déclinaisons"
        return context
    
class ProductItemDetailView(LoginRequiredMixin, DetailView):
    model = ProductItem
    template_name = "detail_item.html"
    context_object_name = "productitem"
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        context = super(ProductItemDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail déclinaison"
        context['attributes'] = self.object.attributes.all()
        return context
    

# ----------- Vues pour Fournisseur -----------

class FournisseurListView(LoginRequiredMixin, ListView):
    model = Fournisseur
    template_name = "list_fournisseurs.html"
    context_object_name = "fournisseurs"
    login_url = '/login/'

    def get_queryset(self):
        return Fournisseur.objects.all()

    def get_context_data(self, **kwargs):
        context = super(FournisseurListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des fournisseurs"
        return context


class FournisseurDetailView(LoginRequiredMixin, DetailView):
    model = Fournisseur
    template_name = "detail_fournisseur.html"
    context_object_name = "fournisseur"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(FournisseurDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du fournisseur"
        return context


class FournisseurCreateView(LoginRequiredMixin, CreateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = "new_fournisseur.html"
    login_url = '/login/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        fournisseur = form.save()
        return redirect('fournisseur-detail', fournisseur.id)


class FournisseurUpdateView(LoginRequiredMixin, UpdateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = "update_fournisseur.html"
    login_url = '/login/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        fournisseur = form.save()
        return redirect('fournisseur-detail', fournisseur.id)


class FournisseurDeleteView(LoginRequiredMixin, DeleteView):
    model = Fournisseur
    template_name = "fournisseur_delete.html"
    success_url = reverse_lazy('fournisseur-list')
    login_url = '/login/'


# ----------- Vues pour Commande -----------

class CommandeListView(LoginRequiredMixin, ListView):
    model = Commande
    template_name = "list_commandes.html"
    context_object_name = "commandes"
    login_url = '/login/'
    
    def get_queryset(self):
        return Commande.objects.select_related('fournisseur')

    def get_context_data(self, **kwargs):
        context = super(CommandeListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des commandes"
        return context
    
    def post(self, request, *args, **kwargs):
        if 'mark_received' in request.POST:
            commande_id = request.POST.get('commande_id')
            commande = get_object_or_404(Commande, pk=commande_id)
            if commande.status != 2:
                commande.date_reception = timezone.now()
                commande.status = 2
                commande.save()
                
                commande.reception_commande()
                
                messages.success(request, 'La commande a été marquée comme reçue, et le stock a été mis à jour.')
            else:
                messages.error(request, 'Cette commande est déjà marquée comme reçue.')
        return redirect('commande-list')

class CommandeDetailView(LoginRequiredMixin, DetailView):
    model = Commande
    template_name = "detail_commande.html"
    context_object_name = "commande"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(CommandeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la commande"
        context['produits'] = CommandeProduit.objects.filter(commande=self.object)
        return context


class CommandeCreateView(LoginRequiredMixin, CreateView):
    model = Commande
    form_class = CommandeForm
    template_name = "new_commande.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['commandeproduit_formset'] = CommandeProduitFormSet(self.request.POST)
        else:
            data['commandeproduit_formset'] = CommandeProduitFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        commandeproduit_formset = context['commandeproduit_formset']
        with transaction.atomic():
            self.object = form.save()
            if commandeproduit_formset.is_valid():
                commandeproduit_formset.instance = self.object
                commandeproduit_formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('commande-detail', kwargs={'pk': self.object.pk})


class CommandeUpdateView(LoginRequiredMixin, UpdateView):
    model = Commande
    form_class = CommandeForm
    template_name = "update_commande.html"
    login_url = '/login/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        commande = form.save()
        return redirect('commande-detail', commande.id)


class CommandeDeleteView(LoginRequiredMixin, DeleteView):
    model = Commande
    template_name = "commande_delete.html"
    success_url = reverse_lazy('commande-list')
    login_url = '/login/'


# ----------- Vues pour CommandeProduit -----------

class CommandeProduitListView(LoginRequiredMixin, ListView):
    model = CommandeProduit
    template_name = "list_commandeproduits.html"
    context_object_name = "commandeproduits"
    login_url = '/login/'

    def get_queryset(self):
        return CommandeProduit.objects.select_related('commande', 'produit')

    def get_context_data(self, **kwargs):
        context = super(CommandeProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des produits commandés"
        return context


class CommandeProduitDetailView(LoginRequiredMixin, DetailView):
    model = CommandeProduit
    template_name = "detail_commandeproduit.html"
    context_object_name = "commandeproduit"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(CommandeProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit commandé"
        return context


class CommandeProduitCreateView(LoginRequiredMixin, CreateView):
    model = CommandeProduit
    form_class = CommandeProduitForm
    template_name = "new_commandeproduit.html"
    login_url = '/login/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        commandeproduit = form.save()
        return redirect('commandeproduit-detail', commandeproduit.id)


class CommandeProduitUpdateView(LoginRequiredMixin, UpdateView):
    model = CommandeProduit
    form_class = CommandeProduitForm
    template_name = "update_commandeproduit.html"
    login_url = '/login/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        commandeproduit = form.save()
        return redirect('commandeproduit-detail', commandeproduit.id)


class CommandeProduitDeleteView(LoginRequiredMixin, DeleteView):
    model = CommandeProduit
    template_name = "commandeproduit_delete.html"
    success_url = reverse_lazy('commandeproduit-list')
    login_url = '/login/'
    
    
    
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Fournisseur, Commande, CommandeProduit
from .forms import CommandeForm, CommandeProduitFormSet
from django.db import transaction

def commander_produit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    fournisseur = get_object_or_404(Fournisseur, id=1)
    
    if request.method == 'POST':
        commande_form = CommandeForm(request.POST)
        commandeproduit_formset = CommandeProduitFormSet(request.POST)
        
        if commande_form.is_valid() and commandeproduit_formset.is_valid():
            with transaction.atomic():
                commande = commande_form.save(commit=False)
                commande.fournisseur = fournisseur
                commande.save()

                commandeproduit_formset.instance = commande
                commandeproduit_formset.save()

            return redirect('commande-detail', commande.id)
    else:
        commande_form = CommandeForm()
        commandeproduit_formset = CommandeProduitFormSet()

    return render(request, 'commande_produit.html', {
        'commande_form': commande_form,
        'commandeproduit_formset': commandeproduit_formset,
        'product': product
    })


class FournisseurListView(LoginRequiredMixin, ListView):
    model = Fournisseur
    template_name = 'list_fournisseurs.html'
    context_object_name = 'fournisseurs'
    login_url = '/login/'

class FournisseurDetailView(LoginRequiredMixin, DetailView):
    model = Fournisseur
    template_name = 'detail_fournisseur.html'
    context_object_name = 'fournisseur'
    login_url = '/login/'

class FournisseurCreateView(LoginRequiredMixin, CreateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = 'new_fournisseur.html'
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('fournisseur-list')

class FournisseurUpdateView(LoginRequiredMixin, UpdateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = 'update_fournisseur.html'
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('fournisseur-list')

class FournisseurDeleteView(LoginRequiredMixin, DeleteView):
    model = Fournisseur
    template_name = 'fournisseur_delete.html'
    success_url = reverse_lazy('fournisseur-list')
    login_url = '/login/'
