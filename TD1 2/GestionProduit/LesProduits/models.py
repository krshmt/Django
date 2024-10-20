from django.db import models
from django.utils import timezone

PRODUCT_STATUS = (
    (0, 'Hors ligne'),
    (1, 'En ligne'),
    (2, 'Rupture de stock'),              
)

COMMANDE_STATUS = (
    (0, 'En préparation'),
    (1, 'Passée'),
    (2, 'Reçue'),
)

"""
    Status : numero, libelle
"""
class Status(models.Model):
    numero  = models.IntegerField()
    libelle = models.CharField(max_length=100)
          
    def __str__(self):
        return "{0} {1}".format(self.numero, self.libelle)
    
"""
Produit : nom, code, etc.
"""
class Product(models.Model):

    class Meta:
        verbose_name = "Produit"

    name          = models.CharField(max_length=100)
    code          = models.CharField(max_length=10, null=True, blank=True, unique=True)
    price_ht      = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire HT")
    price_ttc     = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire TTC")
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0)
    date_creation =  models.DateTimeField(blank=True, verbose_name="Date création")
    stock         = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    
    def save(self, *args, **kwargs):
        if self.stock < 0:
            self.stock = 0
        if self.stock == 0:
            self.status = 2
        else:
            if self.status == 2:
                self.status = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "{0} {1}".format(self.name, self.code)

"""
    Déclinaison de produit déterminée par des attributs comme la couleur, etc.
"""
class ProductItem(models.Model):
    
    class Meta:
        verbose_name = "Déclinaison Produit"

    color   = models.CharField(max_length=100)
    code    = models.CharField(max_length=10, null=True, blank=True, unique=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attributes  = models.ManyToManyField("ProductAttributeValue", related_name="product_item", blank=True)
       
    def __str__(self):
        return "{0} {1}".format(self.color, self.code)
    
class ProductAttribute(models.Model):
    """
    Attributs produit
    """
    
    class Meta:
        verbose_name = "Attribut"
        
    name =  models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class ProductAttributeValue(models.Model):
    """
    Valeurs des attributs
    """
    
    class Meta:
        verbose_name = "Valeur attribut"
        ordering = ['position']
        
    value              = models.CharField(max_length=100)
    product_attribute  = models.ForeignKey('ProductAttribute', verbose_name="Unité", on_delete=models.CASCADE)
    position           = models.PositiveSmallIntegerField("Position", null=True, blank=True)
     
    def __str__(self):
        return "{0} [{1}]".format(self.value, self.product_attribute)


"""
    Fournisseur : nom, adresse, etc.
"""
class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.nom


"""
    Commande : fournisseur, produits, état, date réception, etc.
"""
class Commande(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(default=timezone.now)
    status = models.SmallIntegerField(choices=COMMANDE_STATUS, default=0)
    date_reception = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Commande {self.id} - {self.fournisseur.nom}"
    

    def commander(self, fournisseur, quantite):
        """Créer une commande pour ce produit, peu importe le stock"""
        commande = Commande.objects.create(fournisseur=fournisseur, status=0)
        CommandeProduit.objects.create(commande=commande, produit=self, quantite=quantite)
        return f"Produit {self.name} commandé ({quantite} unités) auprès de {fournisseur.nom}"


    def reception_commande(self):
        if self.status == 2:
            for item in self.produits_commande.all():
                produit = item.produit
                produit.stock += item.quantite
                produit.save()
                

"""
    Lien entre Commande et Product (produits commandés)
"""
class CommandeProduit(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="produits_commande")
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.produit.name} - Quantité : {self.quantite}"
