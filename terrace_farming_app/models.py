from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    space = models.CharField(max_length=100)
    password=models.CharField(max_length=100,null=True)

class LoginTbl(AbstractUser):
    usertype=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.username


class Worker(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    proof=models.ImageField()
    status=models.CharField(max_length=100)
    
class Seller(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    proof=models.ImageField()


class Delivery_Boy(models.Model):
   
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    proof=models.ImageField()
    status=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    quantity=models.IntegerField(max_length=100)
    image=models.ImageField()
    description=models.CharField(max_length=100)
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE,null=True)


class Orders(models.Model):
    owner=models.ForeignKey(Users,on_delete=models.CASCADE)
    status=models.CharField(max_length=100)
    delivery_boy = models.ForeignKey(Delivery_Boy, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    

class Cart(models.Model):
    order=models.ForeignKey(Orders,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(max_length=100)
    date=models.DateField()
    

class Payment(models.Model):
    owner=models.ForeignKey(Users,on_delete=models.CASCADE)
    amount=models.CharField(max_length=100)
    date=models.DateField()
    orderid=models.ForeignKey(Orders,on_delete=models.CASCADE)

class Booking(models.Model):
    worker=models.ForeignKey(Worker,on_delete=models.CASCADE)
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    date=models.DateField(null=True)
    status=models.CharField(max_length=100,null=True)

class Chat(models.Model):
    sender=models.CharField(max_length=100,null=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    


    


    



