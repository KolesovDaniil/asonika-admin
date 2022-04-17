from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from asonika_admin.utils import EmptyResponse, ResponseWithStatusAndError

from .models import Category
from .serializers import (
    CategoryParameterSettingsSerializer,
    CategorySerializer,
    CreateCategorySerializer,
    UpdateCategoryParameterSettingsSerializer,
    UpdateCategorySerializer,
)
from .utils import inherit_parameters_from_parent, update_parameters


@extend_schema(tags=['Category'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == 'create':
            return CreateCategorySerializer

        elif self.action == 'update':
            return UpdateCategorySerializer

        return self.serializer_class

    @extend_schema(responses={'204': EmptyResponse, '404': ResponseWithStatusAndError})
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        request=CreateCategorySerializer,
        responses={'201': CategorySerializer, '4XX': ResponseWithStatusAndError},
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        category = request_serializer.save()
        inherit_parameters_from_parent(category)

        response_serializer = self.serializer_class(
            category, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=UpdateCategorySerializer,
        responses={'204': EmptyResponse, '4XX': ResponseWithStatusAndError},
    )
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        category = self.get_object()
        request_serializer = self.get_serializer(category, data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()
        request_parameters_uuids = request_serializer.validated_data.get('parameters')
        if request_parameters_uuids:
            update_parameters(category, request_parameters_uuids)

        response_serializer = self.serializer_class(
            category, context=self.get_serializer_context()
        )

        return Response(response_serializer.data)

    @extend_schema(
        responses={
            '200': CategoryParameterSettingsSerializer(many=True),
            '4XX': ResponseWithStatusAndError,
        }
    )
    @action(
        methods=['GET'],
        url_path='parameters-settings',
        url_name='parameters-settings',
        detail=True,
    )
    def parameters_settings(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        category = self.get_object()
        parameters_settings = category.categoryparameterssettings_set.all()
        response_serializer = CategoryParameterSettingsSerializer(
            parameters_settings, many=True, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=UpdateCategoryParameterSettingsSerializer(many=True),
        responses={
            '200': CategoryParameterSettingsSerializer(many=True),
            '4XX': ResponseWithStatusAndError,
        },
    )
    @parameters_settings.mapping.put
    def update_parameters_settings(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        category = self.get_object()
        request_serializer = UpdateCategoryParameterSettingsSerializer(
            data=request.data, many=True
        )
        request_serializer.is_valid(raise_exception=True)

        for parameter_settings in request_serializer.validated_data:
            settings = parameter_settings['settings']
            parameter = parameter_settings['parameter']

            # Update settings
            category.categoryparameterssettings_set.filter(
                category=category, parameter=parameter
            ).update(**settings)

        parameters_settings = category.categoryparameterssettings_set.all()
        response_serializer = CategoryParameterSettingsSerializer(
            parameters_settings, many=True, context=self.get_serializer_context()
        )

        return Response(response_serializer.data, status=status.HTTP_200_OK)
