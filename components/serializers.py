from typing import Union

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from categories.models import Category
from categories.serializers import CategoryParameterSettingsSerializer
from manufacturers.models import Manufacturer
from manufacturers.serializers import ManufacturerSerializer
from parameters.models import ListParameter, NumericParameter, Parameter
from specifications.models import Specification
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
            category.categoryparameterssettings_set.all(), many=True
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


class NumericParametersSerializer(serializers.Serializer):
    parameter = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Parameter.objects.all()
    )
    value = serializers.FloatField()


class ListParametersSerializer(serializers.Serializer):
    parameter = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Parameter.objects.all()
    )
    value = serializers.ListSerializer(child=serializers.CharField())


class CreateComponentSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Category.objects.all()
    )
    manufacturer = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Manufacturer.objects.all()
    )
    specification = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Specification.objects.all()
    )
    numeric_parameters = NumericParametersSerializer(many=True, required=False)
    list_parameters = ListParametersSerializer(many=True, required=False)

    def create(self, validated_data: dict) -> Component:
        component = _create_component(validated_data)
        return component

    class Meta:
        model = Component
        fields = [
            'name',
            'category',
            'manufacturer',
            'specification',
            'numeric_parameters',
            'list_parameters',
        ]


class UpdateComponentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    manufacturer = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Manufacturer.objects.all(), required=False
    )
    specification = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Specification.objects.all(), required=False
    )
    numeric_parameters = NumericParametersSerializer(many=True, required=False)
    list_parameters = ListParametersSerializer(many=True, required=False)

    def update(self, instance: Component, validated_data: dict) -> Component:
        component = _update_component(instance, validated_data)
        return component

    class Meta:
        model = Component
        fields = [
            'name',
            'manufacturer',
            'specification',
            'numeric_parameters',
            'list_parameters',
        ]


def _create_component(validated_data: dict) -> Component:
    name = validated_data['name']
    category = validated_data['category']
    manufacturer = validated_data['manufacturer']
    specification = validated_data['specification']
    numeric_parameters = validated_data.get('numeric_parameters', [])
    list_parameters = validated_data.get('list_parameters', [])

    component = Component(
        name=name,
        category=category,
        manufacturer=manufacturer,
        specification=specification,
    )
    component.save()

    for parameter_data in numeric_parameters:
        parameter = parameter_data['parameter']
        value = parameter_data['value']
        numeric_parameter_x_value = NumericParameter(
            parameter=parameter, component=component, value=value
        )
        numeric_parameter_x_value.save()

    for parameter_data in list_parameters:
        parameter = parameter_data['parameter']
        value = parameter_data['value']
        list_parameter_x_value = ListParameter(
            parameter=parameter, component=component, value=value
        )
        list_parameter_x_value.save()

    return component


def _update_component(component: Component, validated_data: dict) -> Component:
    name = validated_data.get('name')
    manufacturer = validated_data.get('manufacturer')
    specification = validated_data.get('specification')
    numeric_parameters = validated_data.get('numeric_parameters')
    list_parameters = validated_data.get('list_parameters')

    if name:
        component.name = name

    if manufacturer:
        component.manufacturer = manufacturer

    if specification:
        component.specification = specification

    if numeric_parameters:
        for parameter_data in numeric_parameters:
            parameter = parameter_data['parameter']
            value = parameter_data['value']
            try:
                component.numericparameter_set.update_or_create(
                    parameter=parameter, defaults={'value': value}
                )
            except Parameter.DoesNotExist:
                raise NotFound(
                    f'Category: {component.category.uuid} '
                    f'does not contain Parameter: {parameter.uuid}'
                )

    if list_parameters:
        for parameter_data in list_parameters:
            parameter = parameter_data['parameter']
            value = parameter_data['value']
            try:
                component.listparameter_set.update_or_create(
                    parameter=parameter, defaults={'value': value}
                )
            except Parameter.DoesNotExist:
                raise NotFound(
                    f'Category: {component.category.uuid} '
                    f'does not contain Parameter: {parameter.uuid}'
                )

    return component
