from django import forms
from LesProduits.models import Product, Fournisseur, Commande, CommandeProduit

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

# Formulaire pour le modèle Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'price_ht', 'price_ttc', 'status', 'date_creation']

# Formulaire pour le modèle Fournisseur
class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'adresse', 'email', 'telephone']

# Formulaire pour le modèle Commande
class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['fournisseur', 'date_commande', 'status', 'date_reception']

# Formulaire pour le modèle CommandeProduit
class CommandeProduitForm(forms.ModelForm):
    class Meta:
        model = CommandeProduit
        fields = ['commande', 'produit', 'quantite']
        search_fields = ["produit__name", "commande__fournisseur__nom"]
