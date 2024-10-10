from django.contrib import admin
from django.utils import timezone
from django import forms
from django.shortcuts import render, redirect
from django.urls import path
from .models import Product, ProductAttribute, ProductAttributeValue, ProductItem, Fournisseur, Commande, CommandeProduit
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME

# Formulaire personnalisé pour passer une commande
class CommandeForm(forms.Form):
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.all(), label="Fournisseur", required=True)
    quantite = forms.IntegerField(min_value=1, label="Quantité à commander", required=True)

# Admin pour les éléments de ProductItem dans Product
class ProductItemAdmin(admin.TabularInline):
    model = ProductItem
    filter_vertical = ("attributes",)

# Action pour changer le statut des produits en "Online"
def set_product_online(modeladmin, request, queryset):
    queryset.update(status=1)
set_product_online.short_description = "Mettre en ligne"

# Action pour changer le statut des produits en "Offline"
def set_product_offline(modeladmin, request, queryset):
    queryset.update(status=0)
set_product_offline.short_description = "Mettre hors ligne"

# Admin pour Product
class ProductAdmin(admin.ModelAdmin):
    actions = [set_product_online, set_product_offline, 'recommander_produit']  # Ajout de l'action "Recommander"
    model = Product
    inlines = [ProductItemAdmin]
    list_filter = ("status",)
    date_hierarchy = 'date_creation'
    list_display = ["code", "name", "price_ht", "price_ttc", "tax", "stock"]
    list_editable = ["name", "price_ht", "price_ttc"]
    
    def recommander_produit(self, request, queryset):
        selected = request.POST.getlist(ACTION_CHECKBOX_NAME)
        return redirect('admin:recommander_produit', selected_ids=",".join(selected))
    recommander_produit.short_description = "Recommander les produits sélectionnés"

    def recommander_produit_view(self, request, selected_ids):
        selected_ids = selected_ids.split(",")
        queryset = Product.objects.filter(pk__in=selected_ids)

        if request.method == 'POST':
            form = CommandeForm(request.POST)
            if form.is_valid():
                fournisseur = form.cleaned_data['fournisseur']
                quantite = form.cleaned_data['quantite']

                # Créer une seule Commande pour tous les produits sélectionnés
                commande = Commande.objects.create(fournisseur=fournisseur, status=0)
                for product in queryset:
                    CommandeProduit.objects.create(commande=commande, produit=product, quantite=quantite)
                self.message_user(request, f"Commande passée pour {len(queryset)} produit(s) auprès de {fournisseur.nom}")

                return redirect('admin:LesProduits_commande_changelist')
        else:
            form = CommandeForm()

        return render(request, 'admin/recommander_produit.html', {'form': form, 'products': queryset})
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('recommander-produit/<str:selected_ids>/', self.admin_site.admin_view(self.recommander_produit_view), name='recommander_produit'),
        ]
        return custom_urls + urls

    def tax(self, instance):
        if instance.price_ht and instance.price_ttc:
            return ((instance.price_ttc / instance.price_ht) - 1) * 100
        return "N/A"
    
    tax.short_description = "Taxes (%)"
    tax.admin_order_field = "price_ht"

# Admin pour Fournisseur
class FournisseurAdmin(admin.ModelAdmin):
    model = Fournisseur
    list_display = ["nom", "adresse", "email", "telephone"]
    search_fields = ["nom", "email"]

# Filtre pour les commandes par état
class CommandeFilter(admin.SimpleListFilter):
    title = 'État de la commande'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            (0, 'En préparation'),
            (1, 'Passée'),
            (2, 'Reçue'),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(status=self.value())

# Actions pour changer l'état des commandes
def set_commande_status_preparation(modeladmin, request, queryset):
    queryset.update(status=0)
set_commande_status_preparation.short_description = "Mettre en préparation"

def set_commande_status_passee(modeladmin, request, queryset):
    queryset.update(status=1)
set_commande_status_passee.short_description = "Marquer comme passée"

def set_commande_status_recue(modeladmin, request, queryset):
    queryset.update(status=2, date_reception=timezone.now())
    for commande in queryset:
        commande.status = 2
        commande.date_reception = timezone.now()
        commande.reception_commande()
        modeladmin.message_user(request, "Commande marquée comme reçue et stock mis à jour.")
    queryset.update(status=2)
set_commande_status_recue.short_description = "Marquer comme reçue et mettre à jour le stock"


# Admin pour Commande
class CommandeAdmin(admin.ModelAdmin):
    model = Commande
    list_filter = [CommandeFilter]
    list_display = ["id", "fournisseur", "date_commande", "status", "date_reception"]
    actions = [set_commande_status_preparation, set_commande_status_passee, set_commande_status_recue]
    search_fields = ["fournisseur__nom"]

# Admin pour CommandeProduit (produits dans une commande)
class CommandeProduitAdmin(admin.ModelAdmin):
    model = CommandeProduit
    list_display = ["commande", "produit", "quantite"]
    search_fields = ["produit__name", "commande__fournisseur__nom"]

# Enregistrement des modèles dans l'admin
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(CommandeProduit, CommandeProduitAdmin)
