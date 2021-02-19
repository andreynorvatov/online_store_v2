from django.db import models
# from django.template.loader import get_template
# from django.core.mail import EmailMessage
# from store_engine.store_engine.settings import EMAIL_HOST_USER
# from forms import *
# from django.forms.models import model_to_dict

def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data.get('final_price__sum')
    else:
        cart.final_price = 0
    cart.save()


# class SendingEmail:
#     from_email = EMAIL_HOST_USER
#     target_email = []
#
#     def sending_email(self, email):
#         target_email = [email]
#
#         vars={
#
#         }