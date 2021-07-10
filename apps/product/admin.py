from django.contrib import admin

# Register your models here.
from apps.product.models import Location, Product, Vendor, Images, VendorProduct

admin.site.register(Location)
# admin.site.register(Product)
admin.site.register(Vendor)


class ProductImagesInline(admin.TabularInline):
    model = Images

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class ProductVendorInline(admin.TabularInline):
    model = VendorProduct

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline, ProductVendorInline]


admin.site.register(Product, ProductAdmin)
