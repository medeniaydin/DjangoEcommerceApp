from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model):
    message = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)


    def __str__(self):
        return f" user: {self.username}, Message: {self.message}, E-mail: {self.email}"
    

class Product(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name= models.CharField(max_length=200, null=True)
    price = models.FloatField(default=0)
    description = models.TextField(max_length=250,null=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(null=True, blank=True, upload_to='images/' ) 

    def __str__(self):
        return f" Username: {self.username} ,Name: {self.name}, Price: {self.price},  İmage: {self.image}, Stock: {self.stock}"
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 'Product' modelini tanımlamanız gerekebilir.
    quantity = models.PositiveIntegerField(default=1,null=True, )
    

class Cart(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=10, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Ek sipariş detayları burada tanımlanabilir

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"
