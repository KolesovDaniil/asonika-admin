from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from asonika_admin.utils import EmptyResponse, ResponseWithStatusAndError

from .models import Parameter
from .serializers import (
    CreateParameterSerializer,
    ParameterSerializer,
    UpdateParameterSerializer,
)


@extend_schema(tags=['Parameter'])
class ParameterViewSet(ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == 'create':
            return CreateParameterSerializer

        elif self.action == 'update':
            return UpdateParameterSerializer

        return self.serializer_class

    @extend_schema(responses={'204': EmptyResponse, '404': ResponseWithStatusAndError})
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        request=CreateParameterSerializer,
        responses={'201': ParameterSerializer, '4XX': ResponseWithStatusAndError},
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        parameter = request_serializer.save()

        response_serializer = self.serializer_class(
            parameter, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=UpdateParameterSerializer,
        responses={'204': EmptyResponse, '4XX': ResponseWithStatusAndError},
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        parameter = self.get_object()
        request_serializer = self.get_serializer(parameter, data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()

        response_serializer = self.serializer_class(
            parameter, context=self.get_serializer_context()
        )

        return Response(response_serializer.data)
