from http import HTTPStatus

from django.urls import reverse
from funcy import lmap
from pytest import fixture

from asonika_admin.tests.utils import error_response
from measurements.models import MeasurementUnit
from users.tests.factories import UserFactory

from .factories import MeasurementGroupFactory, MeasurementUnitFactory


class MeasurementUnitViewsetTestCase:
    @fixture(autouse=True)
    def setup(self, client):
        self.admin_user = UserFactory.create(is_staff=True)
        self.unit = MeasurementUnitFactory.create()
        client.force_login(self.admin_user)

    def test_anonymous_access(self, client):
        url = reverse('api:measurement_unit-list')
        client.logout()

        response = client.get(url)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == error_response(
            code='not_authenticated',
            message='Authentication credentials were not provided.',
        )

    def test_get_list_of_units(self, client):
        url = reverse('api:measurement_unit-list')

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == lmap(_serialize_measurement_unit, [self.unit])

    def test_get_unit_by_uuid(self, client):
        url = reverse('api:measurement_unit-detail', args=[str(self.unit.uuid)])

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == _serialize_measurement_unit(self.unit)

    def test_create_unit(self, client):
        url = reverse('api:measurement_unit-list')
        group = MeasurementGroupFactory.create()
        unit_data = {
            'name': 'unit_name',
            'multiplier': '10',
            'min_value': 10,
            'min_is_included': True,
            'max_value': 10,
            'max_is_included': True,
            'group': str(group.uuid),
        }

        response = client.post(url, data=unit_data)

        assert response.status_code == HTTPStatus.CREATED
        created_unit = MeasurementUnit.objects.get(uuid=response.json()['uuid'])
        assert response.json() == _serialize_measurement_unit(created_unit)

    def test_update_unit(self, client):
        url = reverse('api:measurement_unit-detail', args=[str(self.unit.uuid)])
        updated_data = {'name': 'another_unit_name', 'multiplier': 10}

        response = client.put(url, data=updated_data)

        self.unit.refresh_from_db()
        assert response.status_code == HTTPStatus.OK
        assert response.json() == _serialize_measurement_unit(
            self.unit, name='another_unit_name', multiplier=10
        )

    def test_delete_unit(self, client):
        url = reverse('api:measurement_unit-detail', args=[str(self.unit.uuid)])

        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not MeasurementUnit.objects.exists()


def _serialize_measurement_unit(unit, **kwargs) -> dict:
    return {
        'group': _serialize_measurement_group(unit.group),
        'uuid': str(unit.uuid),
        'name': unit.name,
        'multiplier': unit.multiplier,
        'min_value': unit.min_value,
        'min_is_included': unit.min_is_included,
        'max_value': unit.max_value,
        'max_is_included': unit.max_is_included,
        **kwargs,
    }


def _serialize_measurement_group(group, **kwargs) -> dict:
    return {
        'uuid': str(group.uuid),
        'name': group.name,
        'description': group.description,
        **kwargs,
    }
