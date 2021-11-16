from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from measurements.views import MeasurementGroupViewSet, MeasurementUnitViewSet

measurements_router = SimpleRouter()
measurements_router.register(
    'unit', MeasurementUnitViewSet, basename='measurement_unit'
)
measurements_router.register(
    'group', MeasurementGroupViewSet, basename='measurement_group'
)

api_urls = [path('measurement/', include(measurements_router.urls))]

urlpatterns = [
    path('api/', include((api_urls, 'measurements'), 'api')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
]
