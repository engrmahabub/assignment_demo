from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_datatables.filters import DatatablesFilterBackend

from api.product.serializers import VendorProductSerializer, LocationSerializer
from apps.product.models import VendorProduct, Location


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('id')
    serializer_class = LocationSerializer


class VendorProductViewSet(viewsets.ModelViewSet):
    queryset = VendorProduct.objects.filter(vendor__location__isnull=False)
    serializer_class = VendorProductSerializer
    filter_backends = (DjangoFilterBackend, DatatablesFilterBackend)

    filter_fields = {
        'vendor__location': ['exact'],
    }

    def get_queryset(self):
        location = self.request.query_params.get('vendor__location', None)
        if not location:
            self.queryset = self.queryset.none()

        return self.queryset
