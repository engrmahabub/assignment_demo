from api.product import views as ProductAPI
from assignment.urls import client_router

client_router.register(r'location', ProductAPI.LocationViewSet)
client_router.register(r'product', ProductAPI.VendorProductViewSet)

urlpatterns = []