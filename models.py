from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
 name=models.CharField(max_length=100,unique=True)
 def __str__(self): return self.name
class Product(models.Model):
 name=models.CharField(max_length=200); description=models.TextField(); price=models.DecimalField(max_digits=10,decimal_places=2); discount=models.DecimalField(max_digits=5,decimal_places=2,default=0); category=models.ForeignKey(Category,on_delete=models.CASCADE); stock=models.PositiveIntegerField(default=10); image=models.ImageField(upload_to='products/',blank=True,null=True); rating=models.DecimalField(max_digits=2,decimal_places=1,default=4.5); created_at=models.DateTimeField(auto_now_add=True)
 @property
 def sale_price(self): return self.price-(self.price*self.discount/100)
 def __str__(self): return self.name
class Order(models.Model):
 STATUS=[('Pending','Pending'),('Processing','Processing'),('Shipped','Shipped'),('Delivered','Delivered'),('Cancelled','Cancelled')]
 user=models.ForeignKey(User,on_delete=models.CASCADE); full_name=models.CharField(max_length=150); address=models.TextField(); city=models.CharField(max_length=80); pincode=models.CharField(max_length=10); mobile=models.CharField(max_length=15); payment_method=models.CharField(max_length=30); total=models.DecimalField(max_digits=12,decimal_places=2); status=models.CharField(max_length=20,choices=STATUS,default='Pending'); created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return f'Order #{self.id}'
class OrderItem(models.Model):
 order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items'); product=models.ForeignKey(Product,on_delete=models.PROTECT); quantity=models.PositiveIntegerField(); price=models.DecimalField(max_digits=10,decimal_places=2)
