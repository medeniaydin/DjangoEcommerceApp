from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from django.http import JsonResponse
from . import models
from . import forms
from .models import CartItem
from django.contrib import messages

# Create your views here.


def store(request):
    all_custom = models.Customer.objects.all()  
    all_product = models.Product.objects.all()
    info_dict = {"custom": all_custom,"product":all_product}
    return render(request,'ecommerceapp/store.html',context=info_dict )
  

def addstore(request):
    if request.POST:
        header = request.POST['header_input']
        price = request.POST['price']
        image = request.FILES["image"]
        models.Product.objects.create(name=header, price=price,image=image)
        return redirect(reverse('ecommerceapp:store'))
    else:   
        return render(request,'ecommerceapp/addstore.html')
  

def add_product(request): 
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Form verilerini veritabanına kaydet
            return redirect('ecommerceapp:store')  # Ürün eklendikten sonra mağaza sayfasına yönlendir
    else:
        form = forms.ProductForm()
    
    return render(request, 'ecommerceapp/addproduct.html', {'form': form})


def cart(request):
    context = {'cart_items' : CartItem.objects.filter(user=request.user)}
    return render(request,'ecommerceapp/cart.html',context )
  
    



def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(models.Product, id=product_id)

        # Check if the user is authenticated (logged in)
        if request.user.is_authenticated:
            # If the user is authenticated, add the product to their cart
            cart_item, item_created = CartItem.objects.get_or_create(user=request.user, product=product)

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()

        else:
            # Handle non-authenticated users (e.g., using cookies)
            cart_product_id = str(product.id)

            # Check if there is a 'cart' in the user's session
            if 'cart' not in request.session:
                request.session['cart'] = {}

            # Check if the product is already in the cart
            if cart_product_id in request.session['cart']:
                request.session['cart'][cart_product_id]['quantity'] += 1
            else:
                request.session['cart'][cart_product_id] = {
                    'quantity': 1,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image.url,
                }

            request.session.modified = True  # Mark the session as modified

        # Now, let's retrieve the cart items for rendering in cart.html
        cart_items = []

        # If the user is authenticated, get the cart items from the database
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)

        # If not authenticated, get the cart items from the session
        elif 'cart' in request.session:
            cart_data = request.session['cart']
            for product_id, item_data in cart_data.items():
                product = models.Product.objects.get(id=int(product_id))
                cart_items.append({
                    'product': product,
                    'quantity': item_data['quantity'],
                })

        return render(request, 'ecommerceapp/cart.html', {'cart_items': cart_items}) 

def deletecart(request,id): 
    cartitem = models.Product.objects.get(pk=id) 
    if request.user == cartitem.username: 
        models.Product.objects.filter(id=id).delete() 
        return redirect("ecommerceapp:cart")