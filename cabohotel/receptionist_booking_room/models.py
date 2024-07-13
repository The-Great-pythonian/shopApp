from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
# upload tank
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
# rooms category table_tank
class RoomsCategory(BaseModel):
    category_name = models.CharField(max_length=100)

# room details table_tank_records
class RoomsDetails(BaseModel):
    category = models.ForeignKey(RoomsCategory, on_delete=models.CASCADE, related_name="pizzas")
    room_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    images = models.ImageField(upload_to ="images")

class ShopperCart(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="ShopperCart")
    payment = models.BooleanField(default=False)

#tank holding personal shoping items where you cn delete items on cart
class CartItems(BaseModel):
    basket = models.ForeignKey(ShopperCart, on_delete=models.CASCADE, related_name="cart_items")
    room = models.ForeignKey(RoomsDetails, on_delete=models.CASCADE)

# order table_tank_records
from datetime import datetime
class Order(BaseModel):
    username = models.CharField(max_length=100)
    Totalprice = models.IntegerField(default=100)
    ShippingFee = models.IntegerField(default=100)
    ItemsList = models.CharField(default='no_items')
    Paymentoption =models.CharField()
    DeliveryAddress = models.CharField(max_length=100)
    OrderDate = models.DateField(default=datetime.now())  #current data as defaultt





