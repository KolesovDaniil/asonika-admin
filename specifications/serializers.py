from uuid import uuid4

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from asonika_admin.utils import ValidatedFileField, join_url_parts

from .models import Specification


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['uuid', 'name', 'specification_file_url', 'description']


class CreateSpecificationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    specification_file = ValidatedFileField()
    description = serializers.CharField(required=False)

    class Meta:
        model = Specification
        exclude = ['uuid']

    def validate_specification_file(self, file: InMemoryUploadedFile) -> str:
        return _upload_file(file)


class UpdateSpecificationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    specification_file = ValidatedFileField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Specification
        exclude = ['uuid']

    def validate_specification_file(self, file: InMemoryUploadedFile) -> str:
        return _upload_file(file)


def _upload_file(file: InMemoryUploadedFile) -> str:
    spec_filename = f'{uuid4()}-{file.name}'
    spec_filepath = join_url_parts(
        settings.SPECIFICATIONS_PATH, spec_filename, trailing_slash=False
    )

    with open(spec_filepath, 'wb') as spec_file:
        for chunk in file.chunks():
            spec_file.write(chunk)

    return spec_filename
