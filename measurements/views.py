from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from asonika_admin.utils import EmptyResponse, ResponseWithStatusAndError

from .models import MeasurementGroup, MeasurementUnit
from .serializers import (
    CreateMeasurementGroupSerializer,
    CreateMeasurementUnitSerializer,
    MeasurementGroupSerializer,
    MeasurementUnitSerializer,
    UpdateMeasurementGroupSerializer,
    UpdateMeasurementUnitSerializer,
)


@extend_schema(tags=['MeasurementUnit'])
class MeasurementUnitViewSet(ModelViewSet):
    queryset = MeasurementUnit.objects.all()
    serializer_class = MeasurementUnitSerializer

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == 'create':
            return CreateMeasurementUnitSerializer

        elif self.action == 'update':
            return UpdateMeasurementUnitSerializer

        return self.serializer_class

    @extend_schema(responses={'204': EmptyResponse, '404': ResponseWithStatusAndError})
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        request=CreateMeasurementUnitSerializer,
        responses={'201': MeasurementUnitSerializer, '4XX': ResponseWithStatusAndError},
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        unit = request_serializer.save()

        response_serializer = self.serializer_class(
            unit, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=UpdateMeasurementUnitSerializer,
        responses={'204': EmptyResponse, '4XX': ResponseWithStatusAndError},
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        unit = self.get_object()
        request_serializer = self.get_serializer(unit, data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()

        response_serializer = self.serializer_class(
            unit, context=self.get_serializer_context()
        )

        return Response(response_serializer.data)


@extend_schema(tags=['MeasurementGroup'])
class MeasurementGroupViewSet(ModelViewSet):
    queryset = MeasurementGroup.objects.all()
    serializer_class = MeasurementGroupSerializer

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == 'update':
            return UpdateMeasurementGroupSerializer

        if self.action == 'create':
            return CreateMeasurementGroupSerializer

        return self.serializer_class

    @extend_schema(responses={'204': EmptyResponse, '404': ResponseWithStatusAndError})
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        request=CreateMeasurementGroupSerializer,
        responses={
            '201': MeasurementGroupSerializer,
            '4XX': ResponseWithStatusAndError,
        },
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        group = request_serializer.save()

        response_serializer = self.serializer_class(
            group, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=UpdateMeasurementGroupSerializer,
        responses={'204': EmptyResponse, '4XX': ResponseWithStatusAndError},
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        group = self.get_object()
        request_serializer = self.get_serializer(group, data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()

        response_serializer = self.serializer_class(
            group, context=self.get_serializer_context()
        )

        return Response(response_serializer.data)
