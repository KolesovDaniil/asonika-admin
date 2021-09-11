from typing import Generator

from django.db import connection
from django.db.utils import ProgrammingError
from funcy import joining

from asonika_ecb.utils import validate_schema

from . import schemas

VARCHAR_LEN = 1024
DATABASE_FIELDS_MAPPING = {
    'integer': 'int',
    'string': f'varchar({VARCHAR_LEN})',
    'date': 'date',
}


class ElectronicComponent:
    class TableDoesNotExist(Exception):
        pass

    class TableAlreadyExists(Exception):
        pass

    def __init__(self, table_name: str):
        self.table_name = table_name
        self._check_that_table_exists()

    def create_child(self, child_table_name: str, data: dict) -> 'ElectronicComponent':
        validate_schema(data, schemas.CREATE_CHILD_COMPONENT_SCHEMA)
        QUERY = self._construct_create_child_query(child_table_name, data)
        try:
            with connection.cursor() as cursor:
                cursor.execute(QUERY)
        except ProgrammingError as e:
            if 'already exists' in str(e):
                raise self.TableAlreadyExists('Table already exists in database')

        return self.__class__(child_table_name)

    def delete(self) -> None:
        # TODO: fix possible sql injection
        DROP_TABLE_QUERY = f'DROP TABLE {self.table_name} CASCADE'  # nosec

        with connection.cursor() as cursor:
            cursor.execute(DROP_TABLE_QUERY)

    def get_descendants(self) -> dict:
        pass

    def _check_that_table_exists(self) -> None:
        # TODO: fix possible sql injection
        TABLE_EXISTENCE_QUERY = (  # nosec
            f"SELECT EXISTS (SELECT FROM information_schema.tables "
            f"WHERE table_name = '{self.table_name}');"
        )
        with connection.cursor() as cursor:
            cursor.execute(TABLE_EXISTENCE_QUERY)
            data = cursor.fetchall()

        if not data[0][0]:
            raise self.TableDoesNotExist('Table does not exists')

    def _construct_create_child_query(self, child_table_name: str, data: dict) -> str:
        @joining(',')
        def get_fields(fields: list) -> Generator:
            for field in fields:
                field_name = field['fieldName']
                field_type = DATABASE_FIELDS_MAPPING[field['fieldType']]

                yield f'{field_name} {field_type}'

        table_fields = get_fields(data['fields'])
        # TODO: fix possible sql injection
        QUERY = (  # nosec
            f"CREATE TABLE {child_table_name}({table_fields}) "
            f"INHERITS ({self.table_name});"
        )

        return QUERY


base_component = ElectronicComponent('base_component')
