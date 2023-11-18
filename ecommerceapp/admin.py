from django.contrib import admin
from . import models

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fieldsts = [
    ('Product Group', {"fields": ["name","price","image","description"]}),
    ('Cart Group', {"fields": [" user","product","quantity"]}),
    ('Order Group', {"fields": [" user","order_number","order_date","total_amount"]}),
    ('User Group', {"fields": ["user",["name","price","image","description"]]}),
    ] 
                                    

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.CartItem, ProductAdmin)
admin.site.register(models.Order, ProductAdmin)


