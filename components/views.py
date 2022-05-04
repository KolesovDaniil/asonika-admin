from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from asonika_admin.utils import EmptyResponse, ResponseWithStatusAndError

from .models import Component
from .serializers import (
    ComponentSerializer,
    CreateComponentSerializer,
    UpdateComponentSerializer,
)


@extend_schema(tags=['Component'])
class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == 'create':
            return CreateComponentSerializer

        elif self.action == 'update':
            return UpdateComponentSerializer

        return self.serializer_class

    @extend_schema(responses={'204': EmptyResponse, '404': ResponseWithStatusAndError})
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        request=CreateComponentSerializer,
        responses={'201': ComponentSerializer, '4XX': ResponseWithStatusAndError},
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        component = request_serializer.save()

        response_serializer = self.serializer_class(
            component, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=UpdateComponentSerializer,
        responses={'204': EmptyResponse, '4XX': ResponseWithStatusAndError},
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        component = self.get_object()
        request_serializer = self.get_serializer(component, data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()

        response_serializer = self.serializer_class(
            component, context=self.get_serializer_context()
        )

        return Response(response_serializer.data)
