from .models import Category


def inherit_parameters_from_parent(category: Category) -> None:
    parent_parameters = category.parent.parameters.exclude(
        uuid__in=category.parameters.values_list('uuid', flat=True)
    )
    category.parameters.add(*list(parent_parameters))


def update_parameters(category: Category, request_parameters_uuids: list[str]) -> None:
    added_parameters_uuids, deleted_parameters_uuids = _parameters_changes(
        category, request_parameters_uuids
    )
    category.parameters.remove(*deleted_parameters_uuids)
    category.parameters.add(*added_parameters_uuids)

    for child_category in category.children.all():
        update_parameters(child_category, request_parameters_uuids)


def _parameters_changes(
    category: Category, request_parameters_uuids: list[str]
) -> tuple[set[str], set[str]]:
    category_parameters_uuids = category.parameters.values_list('uuid', flat=True)
    added_parameters_uuids = set(request_parameters_uuids) - set(
        category_parameters_uuids
    )
    deleted_parameters_uuids = set(category_parameters_uuids) - set(
        request_parameters_uuids
    )

    return added_parameters_uuids, deleted_parameters_uuids
