from django import forms
from django.forms import modelformset_factory, inlineformset_factory

from apps.product.models import Location, Product, Images, VendorProduct, Vendor

from django.forms.formsets import formset_factory


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name',)


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('name', 'location',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name',)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image', 'product')


ImageFormSetCreate = inlineformset_factory(Product, Images, form=ImageForm, fields=['image', ], extra=1, can_delete=True)
ImageFormSetUpdate = inlineformset_factory(Product, Images, form=ImageForm, fields=['image', ], extra=0, can_delete=True)


class VendorPriceForm(forms.ModelForm):
    class Meta:
        model = VendorProduct
        fields = ('vendor', 'price','product')


# VendorPriceFormSet = modelformset_factory(VendorProduct, form=ProductForm, formset=VendorPriceForm, fields=('vendor', 'price'), extra=2, can_delete=True)
VendorPriceFormSetCreate = inlineformset_factory(Product,VendorProduct,form=VendorPriceForm, extra=1,fields=['vendor', 'price'], can_delete=True)
VendorPriceFormSetUpdate = inlineformset_factory(Product,VendorProduct,form=VendorPriceForm, extra=0,fields=['vendor', 'price'], can_delete=True)
