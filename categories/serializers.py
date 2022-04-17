from rest_framework import serializers

from parameters.models import Parameter
from parameters.serializers import ParameterSerializer

from .models import Category


class RelatedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['uuid', 'name', 'description']


class CategorySerializer(serializers.ModelSerializer):
    parameters = ParameterSerializer(many=True)
    children = RelatedCategorySerializer(many=True)
    parent = RelatedCategorySerializer()

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
