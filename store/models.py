from django.conf import settings
from django.db import models
from django.urls import reverse
from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    prod_code = models.IntegerField(max_length=8, unique=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
    
    @property    
    def get_uah_price(self):
          price_uah = convert_money(Money(self.price, 'USD'), 'UAH')
          return price_uah

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='prod_img', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    
    def __str__(self):
        return self.image.url
