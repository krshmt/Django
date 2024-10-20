from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from LesProduits.models import Product, Fournisseur, Commande, CommandeProduit, ProductItem, ProductAttribute, ProductAttributeValue
from LesProduits.forms import ProductForm
from django.contrib.auth.models import User

# Tests des modèles

class TestProduit(TestCase):
    def setUp(self):
        self.utilisateur = User.objects.create_user(username='utilisateur_test', password='12345')
        self.produit = Product.objects.create(
            name='Produit Test',
            code='P123',
            price_ht=100,
            price_ttc=120,
            stock=10,
            date_creation=timezone.now(),
            status=1
        )

    def test_creation_produit(self):
        """Vérifie la création correcte d'un produit."""
        produit = Product.objects.get(name='Produit Test')
        self.assertEqual(produit.code, 'P123')
        self.assertEqual(produit.price_ht, 100)
        self.assertEqual(produit.stock, 10)

    def test_vue_liste_produits(self):
        """Test la vue listant les produits pour un utilisateur connecté."""
        self.client.login(username='utilisateur_test', password='12345')
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Produit Test')
        self.assertTemplateUsed(response, 'listProducts.html')

    def test_stock_jamais_negatif(self):
        """Vérifie que le stock ne peut pas être négatif."""
        self.produit.stock = -5
        self.produit.save()
        self.assertEqual(self.produit.stock, 0)

class TestFournisseur(TestCase):
    def test_creation_fournisseur(self):
        """Vérifie la création correcte d'un fournisseur."""
        fournisseur = Fournisseur.objects.create(nom='Fournisseur Test')
        self.assertEqual(fournisseur.nom, 'Fournisseur Test')

# Tests des vues authentifiées

class TestVuesAuthentifiees(TestCase):
    def test_redirection_si_pas_connecte(self):
        """Vérifie que les utilisateurs non connectés sont redirigés vers la page de connexion."""
        response = self.client.get(reverse('product-list'))
        self.assertRedirects(response, '/login/?next=/product/list')

    def test_redirection_creation_produit(self):
        """Vérifie la redirection lors de la création d'un produit si non connecté."""
        response = self.client.get(reverse('product-add'))
        self.assertRedirects(response, '/login/?next=/product/add/')

# Tests des formulaires

class TestFormulaireProduit(TestCase):
    def test_formulaire_produit_valide(self):
        form_data = {
            'name': 'Produit Test',
            'code': 'P123',
            'price_ht': 100,
            'price_ttc': 120,
            'stock': 10,
            'status': 1,
            'date_creation': timezone.now()
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulaire_produit_invalide(self):
        form_data = {
            'name': '',
            'code': 'P123',
            'price_ht': 100,
            'price_ttc': 120
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())

# Test de la vue de création de produit

class TestCreationProduitVue(TestCase):
    def setUp(self):
        self.utilisateur = User.objects.create_user(username='utilisateur_test', password='12345')

    def test_vue_creation_produit(self):
        """Test pour vérifier que la création de produit via la vue fonctionne."""
        self.client.login(username='utilisateur_test', password='12345')
        form_data = {
            'name': 'Produit Nouveau',
            'code': 'P456',
            'price_ht': 150,
            'price_ttc': 180,
            'stock': 20,
            'status': 1,
            'date_creation': timezone.now()
        }
        response = self.client.post(reverse('product-add'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Produit Nouveau').exists())

# Tests des commandes

class TestCommande(TestCase):
    def setUp(self):
        self.fournisseur = Fournisseur.objects.create(nom='Fournisseur Test')
        self.produit = Product.objects.create(
            name='Produit Test',
            code='P123',
            price_ht=100,
            price_ttc=120,
            stock=10,
            status=1,
            date_creation=timezone.now()
        )
        self.commande = Commande.objects.create(
            fournisseur=self.fournisseur,
            status=0,
            date_commande=timezone.now()
        )
        self.commande_produit = CommandeProduit.objects.create(
            commande=self.commande,
            produit=self.produit,
            quantite=5
        )

    def test_creation_commande(self):
        """Vérifie la création correcte d'une commande."""
        self.assertEqual(self.commande.fournisseur.nom, 'Fournisseur Test')
        self.assertEqual(self.commande.status, 0)

    def test_reception_commande_maj_stock(self):
        """Vérifie que la réception d'une commande met à jour le stock du produit."""
        stock_initial = self.produit.stock
        self.commande.status = 2
        self.commande.reception_commande()
        self.produit.refresh_from_db()
        self.assertEqual(self.produit.stock, stock_initial + self.commande_produit.quantite)

# Tests des déclinaisons de produits

class TestProductItem(TestCase):
    def setUp(self):
        self.produit = Product.objects.create(
            name='Produit Test',
            code='P123',
            price_ht=100,
            price_ttc=120,
            stock=10,
            status=1,
            date_creation=timezone.now()
        )
        self.attribut = ProductAttribute.objects.create(name="Couleur")
        self.valeur_attribut = ProductAttributeValue.objects.create(value="Rouge", product_attribute=self.attribut)
        self.product_item = ProductItem.objects.create(
            product=self.produit,
            color="Rouge",
            code="P123-R"
        )
        self.product_item.attributes.add(self.valeur_attribut)

    def test_creation_product_item(self):
        """Vérifie la création correcte d'une déclinaison de produit."""
        self.assertEqual(self.product_item.color, 'Rouge')
        self.assertEqual(self.product_item.code, 'P123-R')

    def test_product_item_attributs(self):
        """Vérifie que la déclinaison de produit possède les attributs associés."""
        self.assertIn(self.valeur_attribut, self.product_item.attributes.all())
