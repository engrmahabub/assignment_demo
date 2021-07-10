from rest_framework import serializers

from apps.product.models import VendorProduct, Vendor, Product, Images, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        # fields = ('image',)
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class VendorProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name',read_only=True)
    product_images = serializers.SerializerMethodField(read_only=True)
    def get_product_images(self,obj):
        images = obj.product.images.all()
        return ImagesSerializer(images,many=True).data

    class Meta:
        model = VendorProduct
        fields = ('id','price','vendor','product','product_name','product_images')
