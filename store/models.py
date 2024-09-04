from django.db import models
from django.urls import reverse, reverse_lazy

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='products')
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    interaction = models.ForeignKey('Interaction', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'id': self.id})

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Interaction(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Slide(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='slides')

    def __str__(self):
        return self.name

class Feedback(models.Model):
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='feedbacks')

    def __str__(self):
        return self.name

class Order(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateTimeField()
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=25)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    payment = models.ForeignKey('Payment', on_delete=models.PROTECT)
    

class Payment(models.Model):
    token = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
