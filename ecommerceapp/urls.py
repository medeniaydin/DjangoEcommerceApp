from django.urls import path, include
from . import views


app_name = 'ecommerceapp'

urlpatterns = [
    path('',views.store,name="store"), #medeniaydin.com/ecommerceapp/  
    path('addstore/',views.addstore,name="addstore"),#medeniaydin.com/ecommerceapp/addstore
    path('cart/', views.cart,name="cart"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path("deletecart/<int:id>/", views.delete_cart, name="deletecart"),
    path('update-quantity/<int:product_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path("deleteproduct/<int:id>",views.deleteProduct,name="deleteproduct"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('view/<int:id>/',views.view,name="view_product"),
    path('profile/', views.user_profile, name='user_profile'),
    path("edit-product/<int:id>",views.edit_product,name='edit_product'),
    
]

