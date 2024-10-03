from django import forms
from LesProduits.models import Product

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        #fields = '__all__'
        exclude = ('price_ttc', 'status')