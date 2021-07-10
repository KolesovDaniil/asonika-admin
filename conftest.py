from django.db import connection
from pytest import fixture

from asonika_ecb.settings import BASE_COMPONENT_MODEL_NAME


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@fixture(scope='session', autouse=True)
def create_base_component(django_db_setup, django_db_blocker):
    CREATE_UUID_EXTENSION_QUERY = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
    CREATE_TABLE_QUERY = (
        f'CREATE TABLE IF NOT EXISTS {BASE_COMPONENT_MODEL_NAME}'
        f'(uuid uuid DEFAULT uuid_generate_v4 (), PRIMARY KEY (uuid));'
    )
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute(CREATE_UUID_EXTENSION_QUERY)
            cursor.execute(CREATE_TABLE_QUERY)
