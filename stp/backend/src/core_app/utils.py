from django.conf import settings


def frontend_url(url: str, args: list = list) -> str:
    args_url = "/".join(args) if args else ""
    return f"{settings.FRONTEND_URL}/{url}/{args_url}"
