from django.urls import path

from apps.product import views
from assignment.urls import router


router.register(r'product', views.ProductViewSet)
urlpatterns = [
    path('location/', views.LocationListView.as_view(), name='location_list'),
    path('location/create', views.LocationCreateView.as_view(), name='location_create'),
    path('location/edit/<int:pk>', views.LocationEditView.as_view(), name='location_update'),

    path('vendor/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendor/create', views.VendorCreateView.as_view(), name='vendor_create'),
    path('vendor/edit/<int:pk>', views.VendorEditView.as_view(), name='vendor_update'),



    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/create', views.ProductCreateView.as_view(), name='product_create'),
    path('product/edit/<int:pk>', views.ProductEditView.as_view(), name='product_update'),



]
