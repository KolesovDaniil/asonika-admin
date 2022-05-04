from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from categories.views import CategoryViewSet
from components.views import ComponentViewSet
from manufacturers.views import ManufacturerViewSet
from measurements.views import MeasurementGroupViewSet, MeasurementUnitViewSet
from parameters.views import ParameterViewSet
from specifications.views import SpecificationViewSet
from users.views import UserLoginView, UserLogoutView

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

specifications_router = SimpleRouter()
specifications_router.register(
    'specification', SpecificationViewSet, basename='specification'
)
parameters_router = SimpleRouter()
parameters_router.register('parameter', ParameterViewSet, basename='parameter')

categories_router = SimpleRouter()
categories_router.register('category', CategoryViewSet, basename='category')

component_router = SimpleRouter()
component_router.register('component', ComponentViewSet, basename='component')

api_urls = [
    path('measurement/', include(measurements_router.urls)),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('', include(manufacturers_router.urls)),
    path('', include(specifications_router.urls)),
    path('', include(parameters_router.urls)),
    path('', include(categories_router.urls)),
    path('', include(component_router.urls)),
]

urlpatterns = [
    path('api/', include((api_urls, 'api'))),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
]
