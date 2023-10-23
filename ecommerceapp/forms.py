from django import forms
from django.forms import ModelForm
from . import models

class AddStoreForm(forms.Form):
    nickname_input = forms.CharField(label="name",max_length=200)
    price_input = forms.CharField(label="price")
    image_input = forms.ImageField()

class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ["name", "price","image"]    


class AddToForms(forms.Form):
    product = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))