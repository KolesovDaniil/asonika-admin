from typing import Union

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategoryParameterSettingsSerializer
from manufacturers.serializers import ManufacturerSerializer
from parameters.models import ListParameter, NumericParameter
from specifications.serializers import SpecificationSerializer

from .models import Component


class ComponentCategorySerializer(serializers.ModelSerializer):
    parameters = serializers.SerializerMethodField()

    class Meta:
        fields = ['uuid', 'name', 'description', 'parameters']
        model = Category

    @extend_schema_field(CategoryParameterSettingsSerializer(many=True))
    def get_parameters(self, category: Category) -> list:
        return CategoryParameterSettingsSerializer(
            category.categoryparameterssettings_set.all()
        ).data


class ParameterWithValueSerializer(serializers.Serializer):
    parameter_uuid = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_parameter_uuid(
        self, param_x_value: Union[NumericParameter, ListParameter]
    ) -> str:
        return str(param_x_value.parameter_id)

    # TODO: Union[serializers.FloatField, serializers.ListField]
    def get_value(
        self, param_x_value: Union[NumericParameter, ListParameter]
    ) -> Union[float, list]:
        return param_x_value.value


class ComponentSerializer(serializers.ModelSerializer):
    category = ComponentCategorySerializer()
    manufacturer = ManufacturerSerializer()
    specification = SpecificationSerializer()
    parameters_values = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = [
            'uuid',
            'name',
            'category',
            'manufacturer',
            'specification',
            'parameters_values',
        ]

    @extend_schema_field(ParameterWithValueSerializer(many=True))
    def get_parameters_values(self, component: Component) -> list:
        return ParameterWithValueSerializer(component.parameters, many=True).data


# class CreateMeasurementGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MeasurementGroup
#         exclude = ['uuid']
#
#
# class UpdateMeasurementGroupSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=False)
#     description = serializers.CharField(required=False)
#
#     class Meta:
#         model = MeasurementGroup
#         exclude = ['uuid']
