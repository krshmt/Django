from django.db import models

# Create your models here.


"""
Produit : nom, code, etc.
"""
class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True, blank=True)
    prixHT = models.DecimalField(max_digits=8, decimal_places=2)
    date_creation = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    def __unicode__(self):
        return "{0} [{1}]".format(self.name, self.code)

"""
Déclinaison de produit déterminée par des attributs comme la couleur, etc.
"""
class ProductItem(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    color =models.CharField(max_length=100)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    def __unicode__(self):
        return "{{0}} {1} [{{2}}]".format(self.product.name, self.color, self.product.code)