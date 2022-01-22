import os
from typing import Any

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from asonika_admin.utils import EmptyResponse, ResponseWithStatusAndError

from .models import Specification
from .serializers import (
    CreateSpecificationSerializer,
    SpecificationSerializer,
    UpdateSpecificationSerializer,
)


@extend_schema(tags=['Specification'])
class SpecificationViewSet(ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == 'update':
            return UpdateSpecificationSerializer
        if self.action == 'create':
            return CreateSpecificationSerializer
        return self.serializer_class

    @extend_schema(responses={'204': EmptyResponse, '404': ResponseWithStatusAndError})
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        self._delete_deprecated_file()
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        request=CreateSpecificationSerializer,
        responses={'201': SpecificationSerializer, '4XX': ResponseWithStatusAndError},
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        specification = request_serializer.save()

        response_serializer = self.serializer_class(
            specification, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=UpdateSpecificationSerializer,
        responses={'204': EmptyResponse, '4XX': ResponseWithStatusAndError},
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        self._delete_deprecated_file()
        specification = self.get_object()
        request_serializer = self.get_serializer(specification, data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()

        response_serializer = self.serializer_class(
            specification, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def _delete_deprecated_file(self) -> None:
        instance = self.get_object()
        spec_filename = instance.specification_file
        spec_filepath = f'{settings.SPECIFICATIONS_FOLDER}/{spec_filename}'

        if os.path.exists(spec_filepath):
            os.remove(spec_filepath)
