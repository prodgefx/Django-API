from rest_framework.routers import DefaultRouter
from products.viewsets import ProductsViewSet

router = DefaultRouter()
router.register('products-abc', ProductsViewSet, basename='products')

#print(router.urls)

urlpatterns = router.urls