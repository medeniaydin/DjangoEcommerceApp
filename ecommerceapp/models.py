from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model):
    message = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f" user: {self.username}, Message: {self.message}, E-mail: {self.email}"
    

class Product(models.Model):
    name= models.CharField(max_length=200, null=True)
    price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(null=True, blank=True, upload_to='images/' ) 

    def __str__(self):
        return f"Name: {self.name}, Price: {self.price},  İmage: {self.image}, Stock: {self.stock}"
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 'Product' modelini tanımlamanız gerekebilir.
    quantity = models.PositiveIntegerField(default=0,null=True)