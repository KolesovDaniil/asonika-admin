CREATE_CHILD_COMPONENT_SCHEMA = {
    'title': 'create_child_component',
    'description': 'Create child component data',
    'type': 'object',
    'properties': {
        'fields': {
            'description': 'Table fields to create with',
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'fieldName': {'description': 'Field name', 'type': 'string'},
                    'fieldType': {
                        'description': 'Type of field',
                        'type': 'string',
                        'enum': ['integer', 'string', 'date'],
                    },
                },
            },
        }
    },
}
