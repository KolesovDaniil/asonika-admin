from django.conf import settings

from asonika_admin.utils import join_url_parts


def get_specification_url(filename: str) -> str:
    return join_url_parts(
        settings.APP_DOMAIN,
        settings.SPECIFICATIONS_FOLDER,
        filename,
        trailing_slash=False,
        first_slash=False,
    )
