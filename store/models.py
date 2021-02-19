from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone


# User = get_user_model()


# class Customer(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     # name = models.CharField(max_length=150, verbose_name='Имя')
#     phone = models.CharField(max_length=12, verbose_name='Номер телефона')
#     email = models.CharField(max_length=255, verbose_name='E-mail')
#
#     def __str__(self):
#         return f'Покупатель: {self.user}'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Цена')

    def __str__(self):
        return f'Продукт: {self.title}'


class CartProduct(models.Model):
    # user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', null=True, verbose_name='Корзина', on_delete=models.CASCADE,
                             related_name='related_products')
    product = models.ForeignKey(Product, null=True, verbose_name='Товар', on_delete=models.CASCADE)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Общая Цена')

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Продукт: {self.product} (для корзины)'


class Cart(models.Model):
    # owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(default=0, max_digits=9, decimal_places=0, \
                                      verbose_name='Общая Цена')

    # in_order = models.BooleanField(default=False)
    # for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return f'Корзина: {self.id}'

    # def save(self, *args, **kwargs):
    #     cart_data = self.products.aggregate(models.Sum('final_price'))
    #     print(f'Печать cart_data: {cart_data}')
    #     if cart_data.get('final_price__sum'):
    #         self.final_price = cart_data.get('final_price__sum')
    #     else:
    #         self.final_price = 0
    #     super().save(*args, **kwargs)


class Order(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True,
                             blank=True)
    name = models.CharField(max_length=150, verbose_name='Имя', null=False, blank=False)
    phone = models.CharField(max_length=12, verbose_name='Телефон', null=False, blank=False)
    email = models.EmailField(max_length=254, verbose_name='Email', null=False, blank=False)

    def __str__(self):
        return str(self.id)


# from store.models import CartProduct, Cart, Product, Customer
# from django.contrib.auth import get_user_model
# Customer.objects.all()
# User = get_user_model()
# u = User.objects.first()
# customer = Customer.objects.create(user=u, phone='123', email='mail@mail')
# product=Product.objects.first()
# c = Cart.objects.create(owner=customer)
# c = Cart.objects.create(owner=customer, final_price=0)
# c.in_order
# c.for_anonymous_user
# cp = CartProduct.objects.create(product=product, user=customer, cart=c, final_price=product.price)
# cp.qty
# cp.final_price
# c.products.add(cp)
# c.products.all()
# c.related_products.all()
# cp.related_cart.all()

'''   <a href="{% url 'add_to_cart' slug=product.slug %}"
                 class="btn btn-primary">Добавить в
                корзину</a>
                '''
