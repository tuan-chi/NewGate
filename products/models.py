from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=60, default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug, 'pk': self.pk})


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter()


class Product(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=140, unique=True)
    brand = models.CharField(max_length=1400)
    description = models.TextField(max_length=500)
    quality = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    old_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0.00)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    objects = ProductManager()

    class Meta:
        ordering = []

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product-detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def add_order_url(self, **kwargs):
        return reverse('products:add-cart', kwargs={'slug': self.slug})


class OrderManager(models.Manager):
    def queryset(self):
        pass

    def get_product(self):
        pass


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{0} of {1}'.format(self.quantity, self.product.title)


class Order(models.Model):
    STATUES = (('N', 'NEW'), ('P', 'PAID'), ('D', 'DONE'))
    statues = models.CharField(max_length=1, choices=STATUES, default='N')
    # code = models.CharField(max_length=10)
    ordered = models.BooleanField(default=False)
    product = models.ManyToManyField(OrderItem, related_name='order_product')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.product.all())

    # def code_limited(self):
    #     if self.code == 'CX':
    #         if len(self.code) == 10:
    #             return self.code
    #         elif len(self.code) < 10 or len(self.code) > 10:
    #             return 'the code can not be less or higher 10 integer'

