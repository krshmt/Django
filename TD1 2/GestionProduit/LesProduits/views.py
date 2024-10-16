from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from LesProduits.models import Product, ProductAttribute, ProductAttributeValue, ProductItem, Fournisseur, Commande, CommandeProduit
from LesProduits.form import ContactUsForm, ProductForm, FournisseurForm, CommandeForm, CommandeProduitForm
from django.views.generic import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse


# Create your views here.


from django.http import HttpResponse


class AboutView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "A propos de nous"
        return context
    def post(self, request, **kwargs):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = "listProducts.html"
    context_object_name = "products"
    def get_queryset(self ):
        query = self.request.GET.get('search')
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des produits"
        return context

@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = "detail_product.html"
    context_object_name = "product"
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit"
        return context
    
    
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
            return redirect('login')  # Redirige vers la page de connexion après inscription
        else:
            return render(request, 'register.html')

class ConnectView(LoginView):
    template_name = 'login.html'
    
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/LesProduits/product/list')  # Redirige vers la liste des produits (Page par défaut qu'on a choisit)
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
        return ProductAttribute.objects.all().prefetch_related('productattributevalue_set')
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
    def get_queryset(self):
        return ProductItem.objects.select_related('product').prefetch_related('attributes')
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
    

# ----------- Vues pour Fournisseur -----------

class FournisseurListView(ListView):
    model = Fournisseur
    template_name = "list_fournisseurs.html"
    context_object_name = "fournisseurs"

    def get_queryset(self):
        return Fournisseur.objects.all()

    def get_context_data(self, **kwargs):
        context = super(FournisseurListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des fournisseurs"
        return context


class FournisseurDetailView(DetailView):
    model = Fournisseur
    template_name = "detail_fournisseur.html"
    context_object_name = "fournisseur"

    def get_context_data(self, **kwargs):
        context = super(FournisseurDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du fournisseur"
        return context


class FournisseurCreateView(CreateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = "new_fournisseur.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        fournisseur = form.save()
        return redirect('fournisseur-detail', fournisseur.id)


class FournisseurUpdateView(UpdateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = "update_fournisseur.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        fournisseur = form.save()
        return redirect('fournisseur-detail', fournisseur.id)


class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    template_name = "fournisseur_delete.html"
    success_url = reverse_lazy('fournisseur-list')


# ----------- Vues pour Commande -----------

class CommandeListView(ListView):
    model = Commande
    template_name = "list_commandes.html"
    context_object_name = "commandes"

    def get_queryset(self):
        return Commande.objects.select_related('fournisseur')

    def get_context_data(self, **kwargs):
        context = super(CommandeListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des commandes"
        return context


class CommandeDetailView(DetailView):
    model = Commande
    template_name = "detail_commande.html"
    context_object_name = "commande"

    def get_context_data(self, **kwargs):
        context = super(CommandeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la commande"
        context['produits'] = CommandeProduit.objects.filter(commande=self.object)
        return context


class CommandeCreateView(CreateView):
    model = Commande
    form_class = CommandeForm
    template_name = "new_commande.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        commande = form.save()
        return redirect('commande-detail', commande.id)


class CommandeUpdateView(UpdateView):
    model = Commande
    form_class = CommandeForm
    template_name = "update_commande.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        commande = form.save()
        return redirect('commande-detail', commande.id)


class CommandeDeleteView(DeleteView):
    model = Commande
    template_name = "commande_delete.html"
    success_url = reverse_lazy('commande-list')


# ----------- Vues pour CommandeProduit -----------

class CommandeProduitListView(ListView):
    model = CommandeProduit
    template_name = "list_commandeproduits.html"
    context_object_name = "commandeproduits"

    def get_queryset(self):
        return CommandeProduit.objects.select_related('commande', 'produit')

    def get_context_data(self, **kwargs):
        context = super(CommandeProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des produits commandés"
        return context


class CommandeProduitDetailView(DetailView):
    model = CommandeProduit
    template_name = "detail_commandeproduit.html"
    context_object_name = "commandeproduit"

    def get_context_data(self, **kwargs):
        context = super(CommandeProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit commandé"
        return context


class CommandeProduitCreateView(CreateView):
    model = CommandeProduit
    form_class = CommandeProduitForm
    template_name = "new_commandeproduit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        commandeproduit = form.save()
        return redirect('commandeproduit-detail', commandeproduit.id)


class CommandeProduitUpdateView(UpdateView):
    model = CommandeProduit
    form_class = CommandeProduitForm
    template_name = "update_commandeproduit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        commandeproduit = form.save()
        return redirect('commandeproduit-detail', commandeproduit.id)


class CommandeProduitDeleteView(DeleteView):
    model = CommandeProduit
    template_name = "commandeproduit_delete.html"
    success_url = reverse_lazy('commandeproduit-list')