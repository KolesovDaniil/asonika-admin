from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from asonika_admin.utils import EmptyResponse, ResponseWithStatusAndError

from .models import Manufacturer
from .serializers import (
    CreateManufacturerSerializer,
    ManufacturerSerializer,
    UpdateManufacturerSerializer,
)


@extend_schema(tags=['Manufacturer'])
class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == 'create':
            return CreateManufacturerSerializer

        elif self.action == 'update':
            return UpdateManufacturerSerializer

        return self.serializer_class

    @extend_schema(responses={'204': EmptyResponse, '404': ResponseWithStatusAndError})
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        request=CreateManufacturerSerializer,
        responses={'201': ManufacturerSerializer, '4XX': ResponseWithStatusAndError},
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        manufacturer = request_serializer.save()

        response_serializer = self.serializer_class(
            manufacturer, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=UpdateManufacturerSerializer,
        responses={'204': EmptyResponse, '4XX': ResponseWithStatusAndError},
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        manufacturer = self.get_object()
        request_serializer = self.get_serializer(manufacturer, data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()

        response_serializer = self.serializer_class(
            manufacturer, context=self.get_serializer_context()
        )

        return Response(response_serializer.data)
