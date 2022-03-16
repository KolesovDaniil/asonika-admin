from http import HTTPStatus

from django.urls import reverse
from funcy import lmap
from pytest import fixture

from asonika_admin.tests.utils import api_response, error_response
from measurements.tests.factories import MeasurementGroupFactory
from parameters.models import Parameter, ParameterTypes
from users.tests.factories import UserFactory

from .factories import ParameterFactory


class ParameterViewsetTestCase:
    @fixture(autouse=True)
    def setup(self, client):
        self.admin_user = UserFactory.create(is_staff=True)
        self.parameter = ParameterFactory.create()
        client.force_login(self.admin_user)

    def test_anonymous_access(self, client):
        url = reverse('api:parameter-list')
        client.logout()

        response = client.get(url)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == error_response(
            code='not_authenticated',
            message='Authentication credentials were not provided.',
        )

    def test_get_list_of_parameters(self, client):
        url = reverse('api:parameter-list')

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == api_response(
            lmap(_serialize_parameter, [self.parameter])
        )

    def test_get_parameter_by_uuid(self, client):
        url = reverse('api:parameter-detail', args=[str(self.parameter.uuid)])

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == api_response(_serialize_parameter(self.parameter))

    def test_create_parameter(self, client):
        url = reverse('api:parameter-list')
        measurement_group = MeasurementGroupFactory.create()
        parameter_data = {
            'type': ParameterTypes.FLOAT.value,
            'name': 'parameter_name',
            'description': 'parameter description',
            'measurement_group': str(measurement_group.uuid),
        }

        response = client.post(url, data=parameter_data)

        created_parameter = Parameter.objects.get(uuid=response.json()['data']['uuid'])
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == api_response(_serialize_parameter(created_parameter))

    def test_update_parameter(self, client):
        url = reverse('api:parameter-detail', args=[str(self.parameter.uuid)])
        updated_data = {
            'name': 'another_parameter_name',
            'type': ParameterTypes.LIST.value,
        }

        response = client.put(url, data=updated_data)

        self.parameter.refresh_from_db()
        assert response.status_code == HTTPStatus.OK
        assert response.json() == api_response(
            _serialize_parameter(
                self.parameter,
                name='another_parameter_name',
                type=ParameterTypes.LIST.value,
            )
        )

    def test_delete_parameter(self, client):
        url = reverse('api:parameter-detail', args=[str(self.parameter.uuid)])

        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not Parameter.objects.exists()


def _serialize_parameter(parameter, **kwargs) -> dict:
    return {
        'measurement_group': _serialize_measurement_group(parameter.measurement_group),
        'uuid': str(parameter.uuid),
        'type': parameter.type,
        'name': parameter.name,
        'description': parameter.description,
        **kwargs,
    }


def _serialize_measurement_group(group, **kwargs) -> dict:
    return {
        'uuid': str(group.uuid),
        'name': group.name,
        'description': group.description,
        **kwargs,
    }
