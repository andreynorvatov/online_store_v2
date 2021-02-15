from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView
from django.views.generic import View
from .models import *
from .forms import OrderForm



def products_list(request):
    products = Product.objects.all()
    # customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get()
    return render(request, 'index.html', context={'products': products, 'cart': cart})


class CartView(View):
    def get(self, request, *args, **kwargs):
        # customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get()
        form = OrderForm(request.POST or None)
        return render(request, 'cart.html', context={'cart': cart, 'form': form})


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        # customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get()
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart,
                                                                  product=product,
                                                                  final_price=product.price,
                                                                  product_id=product.id)
        print(f'Печать cart:{cart_product} {created}')
        # print(f'Печать product:{cart_product.get("product")}')
        # print(f'Печать product.price:{cart_product.get("product.price")}')
        if created:
            cart.products.add(cart_product)

        self.cart = cart
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        cart = Cart.objects.get()
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(cart=cart, product=product, product_id=product.id)
        cart.products.remove(cart_product)
        cart_product.delete()
        self.cart = cart
        self.cart.save()
        # print(f'Принт Сработальо')
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(View):
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        cart = Cart.objects.get()
        print(f'Печать cart:{cart}')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(cart=cart, product=product, product_id=product.id)
        qty = int(request.POST.get('qty'))
        print(f'Печать qty:{qty}')
        cart_product.qty = qty
        cart_product.save()
        self.cart = cart
        self.cart.save()
        print(f'Принт Сработальо')
        return HttpResponseRedirect('/cart/')

class MakeOrder(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        cart = Cart.objects.get()
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(cart=cart, product=product, product_id=product.id)
        self.cart = cart
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.name = form.cleaned_data['name']
            new_order.phone = form.cleaned_data['phone']
            new_order.email = form.cleaned_data['email']
            new_order.save()
            new_order.cart = self.cart
            new_order.save()
            messages.add_messages()



