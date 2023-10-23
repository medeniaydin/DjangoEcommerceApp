from django.urls import path
from . import views


app_name = 'ecommerceapp'

urlpatterns = [
    path('',views.store,name="store"), #medeniaydin.com/ecommerceapp/  
    path('addstore/',views.addstore,name="addstore"),#medeniaydin.com/ecommerceapp/addstore
    path('addproduct/', views.add_product, name="addproduct"),
    path('cart/', views.cart,name="cart"),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path("deletecart/<int:id>",views.deletecart,name="deletecart")  
]

