from http import HTTPStatus

from django.urls import reverse
from funcy import lmap
from pytest import fixture

from asonika_admin.tests.utils import api_response, create_file, error_response
from users.tests.factories import UserFactory

from ..models import Specification
from ..utils import get_specification_url
from .factories import SpecificationFactory


class SpecificationViewSetTestCase:
    @fixture(autouse=True)
    def setup(self, client, tmpdir, settings):
        settings.SPECIFICATIONS_PATH = tmpdir
        self.admin_user = UserFactory.create(is_staff=True)
        self.specification = SpecificationFactory.create()
        client.force_login(self.admin_user)

    def test_anonymous_access(self, client):
        url = reverse('api:specification-list')
        client.logout()

        response = client.get(url)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == error_response(
            code='not_authenticated',
            message='Authentication credentials were not provided.',
        )

    def test_get_list_of_specifications(self, client):
        url = reverse('api:specification-list')

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == api_response(
            lmap(_serialize_specification, [self.specification])
        )

    def test_get_specification_by_uuid(self, client):
        url = reverse('api:specification-detail', args=[str(self.specification.uuid)])

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == api_response(
            _serialize_specification(self.specification)
        )

    def test_create_specification(self, mocker, client):
        mocker.patch(
            'specifications.serializers.uuid4'
        ).return_value = '5fcfe7e1-cc8f-4495-847b-8168240bde21'
        url = reverse('api:specification-list')
        specification_data = {
            'name': 'specification_name',
            'specification_file': create_file('some-spec-file', 'pdf'),
            'description': 'some_description',
        }

        response = client.post(url, data=specification_data)

        created_specification = Specification.objects.get(
            uuid=response.json()['data']['uuid']
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == api_response(
            _serialize_specification(
                created_specification,
                name='specification_name',
                description='some_description',
                specification_file_url=get_specification_url(
                    '5fcfe7e1-cc8f-4495-847b-8168240bde21-some-spec-file.pdf'
                ),
            )
        )

    def test_update_specification(self, mocker, client):
        mocker.patch(
            'specifications.serializers.uuid4'
        ).return_value = '5fcfe7e1-cc8f-4495-847b-8168240bde21'
        url = reverse('api:specification-detail', args=[str(self.specification.uuid)])
        updated_data = {
            'name': 'another_name',
            'description': 'some_description',
            'specification_file': create_file('some-spec-file', 'pdf'),
        }

        response = client.put(url, data=updated_data)

        self.specification.refresh_from_db()
        assert response.status_code == HTTPStatus.OK
        assert response.json() == api_response(
            _serialize_specification(
                self.specification,
                name='another_name',
                description='some_description',
                specification_file_url=get_specification_url(
                    '5fcfe7e1-cc8f-4495-847b-8168240bde21-some-spec-file.pdf'
                ),
            )
        )

    def test_delete_specification(self, client):
        url = reverse('api:specification-detail', args=[str(self.specification.uuid)])

        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not Specification.objects.exists()


def _serialize_specification(specification, **kwargs) -> dict:
    return {
        'uuid': str(specification.uuid),
        'name': specification.name,
        'specification_file_url': specification.specification_file_url,
        'description': specification.description,
        **kwargs,
    }
