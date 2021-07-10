from PIL.TiffImagePlugin import IMAGEWIDTH
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.forms import formsets
from django.shortcuts import render

# Create your views here.


# Location
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_datatables.filters import DatatablesFilterBackend

from apps.product.forms import LocationForm, ProductForm, VendorForm, \
    ImageFormSetCreate, VendorPriceFormSetCreate, ImageFormSetUpdate, VendorPriceFormSetUpdate
from apps.product.models import Location, Product, Vendor, Images
from apps.product.serializers import LocationSerializer, ProductSerializer, VendorSerializer


class LocationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'product.view_location'
    model = Location
    template_name = 'location/list.html'


class LocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'product.add_location'
    model = Location
    form_class = LocationForm
    template_name = 'location/create.html'
    success_url = reverse_lazy('location_list')

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = self.request.user
            post.save()
        return super().form_valid(form)


class LocationEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'product.change_location'
    model = Location
    form_class = LocationForm
    template_name = 'location/create.html'
    success_url = reverse_lazy('location_list')

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = self.request.user
            post.save()
        return super().form_valid(form)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = (DjangoFilterBackend, DatatablesFilterBackend)


class VendorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'product.view_vendor'
    model = Vendor
    template_name = 'vendor/list.html'


class VendorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'product.add_vendor'
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor/create.html'
    success_url = reverse_lazy('vendor_list')

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = self.request.user
            post.save()
        return super().form_valid(form)


class VendorEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'product.change_vendor'
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor/create.html'
    success_url = reverse_lazy('vendor_list')

    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = self.request.user
            post.save()
        return super().form_valid(form)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = (DjangoFilterBackend, DatatablesFilterBackend)


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'product.view_product'
    model = Product
    template_name = 'product/list.html'


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'product.add_product'
    model = Product
    form_class = ProductForm
    # formsets = ImageFormSet
    template_name = 'product/create.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_formset'] = ImageFormSetCreate(self.request.POST,self.request.FILES)
            data['vendor_formset'] = VendorPriceFormSetCreate(self.request.POST)
        else:
            data['image_formset'] = ImageFormSetCreate()
            data['vendor_formset'] = VendorPriceFormSetCreate()

        data['kwargs'] = self.kwargs
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        vendor_formset = context['vendor_formset']
        with transaction.atomic():

            if form.is_valid() and image_formset.is_valid() and vendor_formset.is_valid():
                product = form.save(commit=False)
                product.created_by = self.request.user
                self.object = product.save()

                if product:
                    for image in image_formset:
                        img = image.save(commit=False)
                        img.product = product
                        img.save()

                    for vendor_product_price in vendor_formset:
                        vp = vendor_product_price.save(commit=False)
                        vp.product = product
                        vp.save()

        return super().form_valid(form)


class ProductEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'product.change_product'
    model = Product
    form_class = ProductForm
    # formsets = ImageFormSet
    template_name = 'product/create.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_formset'] = ImageFormSetUpdate(self.request.POST,self.request.FILES)
            data['vendor_formset'] = VendorPriceFormSetUpdate(self.request.POST)
        else:
            data['image_formset'] = ImageFormSetUpdate(instance=self.object)
            data['vendor_formset'] = VendorPriceFormSetUpdate(instance=self.object)
            # OrderDetailsUpdateFormset(instance=self.object)

        data['kwargs'] = self.kwargs
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        vendor_formset = context['vendor_formset']
        print(form.is_valid(), image_formset.is_valid(), vendor_formset.is_valid())
        # print(vendor_formset.cleaned_data)
        with transaction.atomic():

            if form.is_valid():
                product = form.save(commit=False)
                product.created_by = self.request.user
                self.object = product.save()

                if product:
                    if image_formset.is_valid():
                        for image in image_formset:
                            img = image.save(commit=False)
                            img.product = product
                            img.save()
                    if vendor_formset.is_valid():
                        for vendor_product_price in vendor_formset:
                            vp = vendor_product_price.save(commit=False)
                            vp.product = product
                            vp.save()
                    else:
                        for vendor_product_price in vendor_formset:
                            print(vendor_product_price.cleaned_data)

        return super().form_valid(form)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(vendor__location__isnull=False)
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, DatatablesFilterBackend)

    def get_queryset(self):
        location = self.request.query_params.get('location', None)
        if location:
            self.queryset = self.queryset.filter(vendor__location=location)

        return self.queryset


class VendorProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(vendor__location__isnull=False)
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, DatatablesFilterBackend)

    def get_queryset(self):
        location = self.request.query_params.get('location', None)
        if location:
            self.queryset = self.queryset.filter(vendor__location=location)

        return self.queryset
