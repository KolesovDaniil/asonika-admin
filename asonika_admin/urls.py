from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from manufacturers.views import ManufacturerViewSet
from measurements.views import MeasurementGroupViewSet, MeasurementUnitViewSet

measurements_router = SimpleRouter()
measurements_router.register(
    'unit', MeasurementUnitViewSet, basename='measurement_unit'
)
measurements_router.register(
    'group', MeasurementGroupViewSet, basename='measurement_group'
)

manufacturers_router = SimpleRouter()
manufacturers_router.register(
    'manufacturer', ManufacturerViewSet, basename='manufacturer'
)

api_urls = [
    path('measurement/', include(measurements_router.urls)),
    path('manufacturer/', include(manufacturers_router.urls)),
]

urlpatterns = [
    path('api/', include((api_urls, 'measurements'), 'api')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
]
