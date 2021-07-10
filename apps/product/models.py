from django.db import models


# Create your models here.
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class Images (models.Model):
    product = models.ForeignKey(Product, default=None, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.image.url

class Vendor(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(Location, null=False, blank=False, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through="VendorProduct", blank=False, null=False)

    def __str__(self):
        return self.name +' - '+self.location.name


class VendorProduct(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    status = models.BooleanField(default=False)
