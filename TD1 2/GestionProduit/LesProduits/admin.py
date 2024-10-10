from django.contrib import admin
from .models import Product, ProductAttribute, ProductAttributeValue, ProductItem, Fournisseur, Commande, CommandeProduit

# Admin pour les éléments de ProductItem dans Product
class ProductItemAdmin(admin.TabularInline):
    model = ProductItem
    filter_vertical = ("attributes",)

# Filtre personnalisé pour les produits en ligne et hors ligne
class ProductFilter(admin.SimpleListFilter):
    title = 'filtre produit'
    parameter_name = 'custom_status'

    def lookups(self, request, model_admin):
        return (
            ('online', 'En ligne'),
            ('offline', 'Hors ligne'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'online':
            return queryset.filter(status=1)
        if self.value() == 'offline':
            return queryset.filter(status=0)

# Actions pour changer le statut d'un produit
def set_product_online(modeladmin, request, queryset):
    queryset.update(status=1)
set_product_online.short_description = "Mettre en ligne"

def set_product_offline(modeladmin, request, queryset):
    queryset.update(status=0)
set_product_offline.short_description = "Mettre hors ligne"

# Admin pour Product
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductItemAdmin]
    list_filter = (ProductFilter,)
    date_hierarchy = 'date_creation'
    actions = [set_product_online, set_product_offline]
    list_display = ["code", "name", "price_ht", "price_ttc", "tax", "stock"]
    list_editable = ["name", "price_ht", "price_ttc"]

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
    for commande in queryset:
        commande.status = 2
        commande.date_reception = timezone.now()
        commande.reception_commande()
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
