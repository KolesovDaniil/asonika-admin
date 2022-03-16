from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from measurements.models import MeasurementGroup
from measurements.serializers import MeasurementGroupSerializer

from .models import Parameter


class UpdateParameterSerializer(serializers.ModelSerializer):
    type = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    measurement_group = serializers.SlugRelatedField(
        slug_field='uuid', queryset=MeasurementGroup.objects.all(), required=False
    )

    class Meta:
        model = Parameter
        exclude = ['uuid']


class CreateParameterSerializer(serializers.ModelSerializer):
    measurement_group = serializers.SlugRelatedField(
        slug_field='uuid', queryset=MeasurementGroup.objects.all()
    )

    class Meta:
        model = Parameter
        exclude = ['uuid']


class ParameterSerializer(serializers.ModelSerializer):
    measurement_group = serializers.SerializerMethodField()

    @extend_schema_field(MeasurementGroupSerializer)
    def get_measurement_group(self, parameter: Parameter) -> dict:
        return MeasurementGroupSerializer(parameter.measurement_group).data

    class Meta:
        model = Parameter
        fields = ['uuid', 'type', 'name', 'description', 'measurement_group']
