from http import HTTPStatus

from django.urls import reverse
from funcy import lmap
from pytest import fixture

from asonika_admin.tests.utils import api_response, error_response
from manufacturers.models import Manufacturer
from users.tests.factories import UserFactory

from .factories import ManufacturerFactory


class ManufacturerViewTestCase:
    @fixture(autouse=True)
    def setup(self, client):
        self.admin_user = UserFactory.create(is_staff=True)
        self.manufacturer = ManufacturerFactory.create()
        client.force_login(self.admin_user)

    def test_anonymous_access(self, client):
        url = reverse('api:manufacturer-list')
        client.logout()

        response = client.get(url)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == error_response(
            code='not_authenticated',
            message='Authentication credentials were not provided.',
        )

    def test_get_list_of_manufacturers(self, client):
        url = reverse('api:manufacturer-list')

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == api_response(
            lmap(_serialize_manufacturer, [self.manufacturer])
        )

    def test_get_manufacturer_by_uuid(self, client):
        url = reverse('api:manufacturer-detail', args=[str(self.manufacturer.uuid)])

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == api_response(
            _serialize_manufacturer(self.manufacturer)
        )

    def test_create_manufacturer(self, client):
        url = reverse('api:manufacturer-list')
        manufacturer_data = {'name': 'group_name', 'description': 'some_description'}

        response = client.post(url, data=manufacturer_data)

        assert response.status_code == HTTPStatus.CREATED
        created_manufacturer = Manufacturer.objects.get(
            uuid=response.json()['data']['uuid']
        )
        assert response.json() == api_response(
            _serialize_manufacturer(created_manufacturer)
        )

    def test_update_manufacturer(self, client):
        url = reverse('api:manufacturer-detail', args=[str(self.manufacturer.uuid)])
        updated_data = {'name': 'another_name', 'description': 'some_description'}

        response = client.put(url, data=updated_data)

        self.manufacturer.refresh_from_db()
        assert response.status_code == HTTPStatus.OK
        assert response.json() == api_response(
            _serialize_manufacturer(
                self.manufacturer, name='another_name', description='some_description'
            )
        )

    def test_delete_manufacturer(self, client):
        url = reverse('api:manufacturer-detail', args=[str(self.manufacturer.uuid)])

        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not Manufacturer.objects.exists()


def _serialize_manufacturer(manufacturer, **kwargs) -> dict:
    return {
        'uuid': str(manufacturer.uuid),
        'name': manufacturer.name,
        'description': manufacturer.description,
        **kwargs,
    }
