from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from . import models
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required 
from .models import CartItem, Order
from .models import Cart
from .utils import calculate_cart_total
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.views.generic import DetailView
import random
import string

# Create your views here.


def store(request):
    all_custom = models.Customer.objects.all()  
    all_product = models.Product.objects.all()
    info_dict = {"custom": all_custom,"product":all_product}
    return render(request,'ecommerceapp/store.html',context=info_dict )
  
@login_required(login_url="/login")
def addstore(request):
    if request.POST:
        header = request.POST['header_input']
        price = request.POST['price']
        image = request.FILES["image"]
        description = request.POST["description"]
        models.Product.objects.create(username=request.user,name=header, price=price,image=image,description=description)
        return redirect(reverse('ecommerceapp:store'))
    else:   
        return render(request,'ecommerceapp/addstore.html')


@login_required(login_url="/login")
def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_total = calculate_cart_total(cart_items)  # Sepet toplamını hesaplayın
        total_prices = []  # Her bir ürünün toplam fiyatlarını saklamak için bir liste oluşturun

        for item in cart_items:
            total_price = item.product.price * item.quantity
            item.total_display = f"{total_price}"
            total_prices.append(total_price)  # Hesaplanan toplam fiyatı listeye ekleyin

        # Sonuçları context içinde kullanılabilir hale getirin
        context = {
            'cart_items': cart_items,
            'cart_total': cart_total,  # Sepet toplamını şablona gönderin
            'total_prices': total_prices,  # Her bir ürünün toplam fiyatlarını şablona gönderin
        }

        return render(request, 'ecommerceapp/cart.html', context)
    

def view(request, id):
    product_id = str(id)
    product = models.Product.objects.filter(pk=product_id)
    prd_info = {'product': product}
    return render(request, 'ecommerceapp/view.html', context=prd_info)



class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'ecommerceapp/view.html'  # Şablon dosyası adı
    context_object_name = 'product'  # Şablon dosyasında kullanılacak nesne adı



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
                return redirect("ecommerceapp:cart")
            else:
                return redirect("ecommerceapp:cart")

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
         


@login_required
def delete_cart(request, id):
    if request.method == 'POST':
        # Öncelikle, oturumda sepet verilerini kontrol edin
        if 'cart' in request.session:
            cart_data = request.session['cart']
            product_id = str(id)
            if product_id in cart_data:
                del cart_data[product_id]  # Ürünü sepetten kaldır
                request.session.modified = True  # Oturumu güncelle

    # Eğer kullanıcı oturumda giriş yapmışsa, veritabanındaki sepeti güncelleyin
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product_id=id).delete()

    # Silme işlemi tamamlandıktan sonra sepet sayfasına yönlendirin
    return redirect("ecommerceapp:cart")


def update_cart_total(user):
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(user=user)
        total = 0

        for item in cart_items:
            total += item.product.price * item.quantity

        # Kullanıcıya ait sepetteki toplam tutarı güncelle
        cart.total_amount = total
        cart.save()
    except Cart.DoesNotExist:
        # Kullanıcıya ait bir sepet bulunamadı, burada gerekli işlemler yapılabilir
        pass

@login_required
def update_quantity(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(models.Product, id=product_id)
        quantity = int(request.POST.get('quantity'))
        
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            return redirect("ecommerceapp:cart")
        else:
            cart_product_id = str(product.id)

            if 'cart' in request.session:
                cart_product_id = str(product.id)  # İstenilen ID'yi stringe dönüştür
                if cart_product_id in request.session['cart']:
                    request.session['cart'][cart_product_id]['quantity'] = quantity
                    request.session.modified = True

        update_cart_total(request.user)  # Sepet toplamını güncelle

        cart_items = []

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        elif 'cart' in request.session:
            cart_data = request.session['cart']
            for product_id, item_data in cart_data.items():
                product = models.Product.objects.get(id=int(product_id))
                cart_items.append({
                    'product': product,
                    'quantity': item_data['quantity'],
                })
             
        return render(request, 'ecommerceapp/cart.html', {'cart_items': cart_items})
        


def generate_order_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@login_required
def checkout(request):
    if request.method == 'POST':
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        cart_total = calculate_cart_total(cart_items)

        # Burada ödeme sayfasına yönlendirme yapılabilir
        return render(request, 'ecommerceapp/checkout.html', {'cart_total': cart_total, 'cart_items': cart_items})

    return HttpResponseBadRequest("Geçersiz istek")

@login_required
def deleteProduct(request,id):
    product_id = str(id)
    product = models.Product.objects.get(pk=product_id) 
    if request.user == product.username: 
        models.Product.objects.filter(id=product_id).delete()
        return redirect("ecommerceapp:user_profile") 
    
@login_required(login_url="/login")
def user_profile(request):
    if request.user.is_authenticated:
        user_products = models.Product.objects.filter(username=request.user)  # Bu satır, kullanıcının eklediği ürünleri getirecek. Product modeline göre uyarlanmalı.
        return render(request, 'ecommerceapp/user_profile.html', {'user_products': user_products})
    else:
        # Burada isteğe bağlı olarak giriş yapmamış kullanıcılar için bir yönlendirme yapılabilir.
        return render(request, 'registration/login.html')

from django.forms.models import model_to_dict

@login_required(login_url="/login")
def edit_product(request, id):
    product = get_object_or_404(models.Product, id=id)

    if request.method == 'GET':
        form = forms.ProductForm(instance=product)
        return render(request, 'ecommerceapp/edit_product.html', {'form': form, 'product': product})

    elif request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            new_product = form.save(commit=False)  # Veritabanına hemen kaydetmeyin, önce değişiklikleri kontrol edin

            # Kontrol etmek istediğiniz alanlar buraya eklenmeli
            # Eğer yeni bir fotoğraf yüklenmişse veya fotoğraf silinmişse
            if 'image' in form.changed_data or 'image' in request.FILES:
                new_product.image = form.cleaned_data['image']
            elif 'image-clear' in request.POST and request.POST['image-clear'] == 'on':
                new_product.image = None  # Eğer clear checkbox'ı işaretlendiyse, fotoğrafı temizle


            new_product.save()  # Değişiklikleri kaydet
            return redirect("ecommerceapp:user_profile")
            #return HttpResponse(f'Ürün {product.id} başarıyla güncellendi.')

        else:
            return render(request, 'ecommerceapp/edit_product.html', {'form': form, 'product': product})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"   