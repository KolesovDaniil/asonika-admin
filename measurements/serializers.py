from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import MeasurementGroup, MeasurementUnit


class MeasurementGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementGroup
        fields = ['uuid', 'name', 'description']


class CreateMeasurementGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementGroup
        exclude = ['uuid']


class UpdateMeasurementGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = MeasurementGroup
        exclude = ['uuid']


class UpdateMeasurementUnitSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    multiplier = serializers.IntegerField(required=False)
    min_value = serializers.IntegerField(required=False)
    min_is_included = serializers.BooleanField(required=False)
    max_value = serializers.IntegerField(required=False)
    max_is_included = serializers.BooleanField(required=False)
    group = serializers.SlugRelatedField(
        slug_field='uuid', queryset=MeasurementGroup.objects.all(), required=False
    )

    class Meta:
        model = MeasurementUnit
        exclude = ['uuid']


class CreateMeasurementUnitSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field='uuid', queryset=MeasurementGroup.objects.all()
    )

    class Meta:
        model = MeasurementUnit
        exclude = ['uuid']


class MeasurementUnitSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()

    @extend_schema_field(MeasurementGroupSerializer)
    def get_group(self, unit: MeasurementUnit) -> dict:
        return MeasurementGroupSerializer(unit.group).data

    class Meta:
        model = MeasurementUnit
        fields = [
            'uuid',
            'name',
            'multiplier',
            'min_value',
            'min_is_included',
            'max_value',
            'max_is_included',
            'group',
        ]
