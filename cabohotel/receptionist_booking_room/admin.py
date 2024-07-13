from django.contrib import admin
from .models import *
# Register your models here.


class RoomsCategory_format(admin.ModelAdmin):
    list_display = ("category_name",)
#register the tank under him to perform CRUD
admin.site.register(RoomsCategory, RoomsCategory_format)

class RoomsDetails_format(admin.ModelAdmin):
    list_display = ("category","room_name","price","images","category_category_name",)
    #* for freindly name for  foreign keyin  Room category field values  "category_category_name
    def category_category_name(self, instance):
        return instance.category.category_name
#register the tank under him to perform CRUD
admin.site.register(RoomsDetails, RoomsDetails_format)

class ShopperCart_format(admin.ModelAdmin):
    list_display = ("user","payment",)
# #register the tank under him to perform CRUD
admin.site.register(ShopperCart, ShopperCart_format)
#
#
class CartItems_format(admin.ModelAdmin):
    list_display = ("basket","room","basket_user",)
    #for feindly value of foregin key in roomdetails
    def basket_user(self, instance):
        return instance.basket.user
admin.site.register(CartItems, CartItems_format)

class Order_format(admin.ModelAdmin):
    list_display = ("username","Totalprice","ShippingFee","ItemsList","Paymentoption","DeliveryAddress","OrderDate",)
#register the tank under him to perform CRUD
admin.site.register(Order, Order_format)



