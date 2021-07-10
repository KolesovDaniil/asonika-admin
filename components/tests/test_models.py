from pytest import fixture, raises

from asonika_ecb.settings import BASE_COMPONENT_MODEL_NAME
from components.models import ElectronicComponent, base_component


class ElectronicComponentTestCase:
    @fixture(autouse=True)
    def setup(self):
        self.data = {'fields': [{'fieldName': 'voltage', 'fieldType': 'integer'}]}

    def test_get_table_representation(self):
        # base_component model creating in `create_base_component` fixture
        ElectronicComponent(BASE_COMPONENT_MODEL_NAME)

    def test_table_does_not_exists(self):
        with raises(ElectronicComponent.TableDoesNotExist):
            ElectronicComponent('nonexisting_table')

    def test_create_child_component(self):
        resistor = base_component.create_child('resistor', self.data)

        assert resistor.table_name == 'resistor'

    def test_create_2_deep_child_component(self):
        resistor = base_component.create_child('resistor', self.data)
        data = {'fields': [{'fieldName': 'current', 'fieldType': 'integer'}]}
        smd_resistor = resistor.create_child('smd_resistor', data)

        assert smd_resistor.table_name == 'smd_resistor'

    def test_delete_table(self):
        resistor = base_component.create_child('resistor', self.data)

        resistor.delete()

        with raises(ElectronicComponent.TableDoesNotExist):
            ElectronicComponent('resistor')

    def test_delete_table_with_children(self):
        resistor = base_component.create_child('resistor', self.data)
        data = {'fields': [{'fieldName': 'current', 'fieldType': 'integer'}]}
        resistor.create_child('smd_resistor', data)

        resistor.delete()

        with raises(ElectronicComponent.TableDoesNotExist):
            ElectronicComponent('smd_resistor')
