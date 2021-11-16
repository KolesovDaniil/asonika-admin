from http import HTTPStatus

from django.urls import reverse
from funcy import lmap
from pytest import fixture

from asonika_admin.tests.utils import error_response
from measurements.models import MeasurementGroup
from users.tests.factories import UserFactory

from .factories import MeasurementGroupFactory


class MeasurementGroupViewTestCase:
    @fixture(autouse=True)
    def setup(self, client):
        self.admin_user = UserFactory.create(is_staff=True)
        self.group = MeasurementGroupFactory.create()
        client.force_login(self.admin_user)

    def test_anonymous_access(self, client):
        url = reverse('api:measurement_group-list')
        client.logout()

        response = client.get(url)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == error_response(
            code='not_authenticated',
            message='Authentication credentials were not provided.',
        )

    def test_get_list_of_groups(self, client):
        url = reverse('api:measurement_group-list')

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == lmap(_serialize_measurement_group, [self.group])

    def test_get_group_by_uuid(self, client):
        url = reverse('api:measurement_group-detail', args=[str(self.group.uuid)])

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == _serialize_measurement_group(self.group)

    def test_create_group(self, client):
        url = reverse('api:measurement_group-list')
        group_data = {'name': 'group_name', 'description': 'some_description'}

        response = client.post(url, data=group_data)

        assert response.status_code == HTTPStatus.CREATED
        created_group = MeasurementGroup.objects.get(uuid=response.json()['uuid'])
        assert response.json() == _serialize_measurement_group(created_group)

    def test_update_group(self, client):
        url = reverse('api:measurement_group-detail', args=[str(self.group.uuid)])
        updated_data = {'name': 'another_name', 'description': 'some_description'}

        response = client.put(url, data=updated_data)

        self.group.refresh_from_db()
        assert response.status_code == HTTPStatus.OK
        assert response.json() == _serialize_measurement_group(
            self.group, name='another_name', description='some_description'
        )

    def test_delete_group(self, client):
        url = reverse('api:measurement_group-detail', args=[str(self.group.uuid)])

        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not MeasurementGroup.objects.exists()


def _serialize_measurement_group(group, **kwargs) -> dict:
    return {
        'uuid': str(group.uuid),
        'name': group.name,
        'description': group.description,
        **kwargs,
    }
