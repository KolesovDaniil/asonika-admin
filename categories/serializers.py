from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from categories.models import CategoryParametersSettings
from parameters.models import Parameter
from parameters.serializers import ParameterSerializer

from .models import Category


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['uuid', 'name', 'description']


class CategorySerializer(serializers.ModelSerializer):
    parameters = ParameterSerializer(many=True)
    children = SimpleCategorySerializer(many=True)
    parent = SimpleCategorySerializer()

    class Meta:
        model = Category
        fields = ['uuid', 'name', 'description', 'parameters', 'parent', 'children']


class CreateCategorySerializer(serializers.ModelSerializer):
    parameters = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Parameter.objects.all(), many=True
    )
    parent = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Category.objects.all()
    )

    class Meta:
        model = Category
        exclude = ['uuid']


class UpdateCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    parameters = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Parameter.objects.all(), many=True, required=False
    )
    parent = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = Category
        exclude = ['uuid']


class ParameterSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryParametersSettings
        fields = ['required']


class CategoryParameterSettingsSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer()
    settings = serializers.SerializerMethodField()

    class Meta:
        model = CategoryParametersSettings
        fields = ['parameter', 'settings']

    @extend_schema_field(ParameterSettingsSerializer)
    def get_settings(self, parameter_settings: CategoryParametersSettings) -> dict:
        return ParameterSettingsSerializer(parameter_settings).data


class UpdateParameterSettingsSerializer(serializers.ModelSerializer):
    required = serializers.BooleanField(required=False)

    class Meta:
        model = CategoryParametersSettings
        fields = ['required']


class UpdateCategoryParameterSettingsSerializer(serializers.Serializer):
    parameter = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Parameter.objects.all()
    )
    settings = UpdateParameterSettingsSerializer()
