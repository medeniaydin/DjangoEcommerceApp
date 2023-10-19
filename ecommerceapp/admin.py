from django.contrib import admin
from . import models

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fieldsts = [
     ('Product Group', {"fields": ["name","price","image"]}),
    ('Cart Group', {"fields": [" user","product","quantity"]})
    ]
                                    

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.CartItem, ProductAdmin)
