from django.urls import path
from . import views


urlpatterns = [
    path('',views.builder_home, name='home'),
    path('Register/', views.builder_Register, name='Register'),
    path('Login/', views.builder_Login, name='Login'),
    path('addCart/<uuid:X>', views.builder_addCart , name="addCart"),
    path('ShowCart/', views.builder_ShowCart, name='ShowCart'),
    path('RemoveCart/<uuid:X>', views.builder_RemoveCart, name='RemoveCart'),
    path('Checkout/', views.builder_Checkout, name='Checkout'),
    path('Order/', views.builder_Order, name='Order'),
]
#note name='ShowCart' and link >> ShowCart/' must be same else there willbe error

#settings.MEDIA_URL, document_root=settings.MEDIA_ROOT