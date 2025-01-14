from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=150)
    desc=models.TextField()
    image=models.ImageField(upload_to='products/')
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name
    

class Purchase(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    customer_name=models.CharField(max_length=200)
    purchse_date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


    def total_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.product}-{self.customer_name}"
    
class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 