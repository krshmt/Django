from django import forms
from django.forms import inlineformset_factory
from LesProduits.models import Product, Fournisseur, Commande, CommandeProduit

# Formulaire de contact
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
        widgets = {
            'date_commande': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'date_reception': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }

    def __init__(self, *args, **kwargs):
        super(CommandeForm, self).__init__(*args, **kwargs)
        self.fields['date_commande'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['date_reception'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['date_reception'].required = False

# Formulaire pour les produits dans la commande
class CommandeProduitForm(forms.ModelForm):
    class Meta:
        model = CommandeProduit
        fields = ['produit', 'quantite']


# Inline formset pour ajouter plusieurs produits à une commande
CommandeProduitFormSet = inlineformset_factory(
    Commande, 
    CommandeProduit, 
    form=CommandeProduitForm, 
    extra=1,  # Nombre de formulaires supplémentaires par défaut
    can_delete=True
)

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'adresse', 'email', 'telephone']