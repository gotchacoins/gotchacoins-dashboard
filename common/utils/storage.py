from django.conf import settings
from django.core.files.storage import FileSystemStorage

if settings.USE_S3:
    from common.storages.public import PublicMediaStorage
    from common.storages.private import PrivateMediaStorage


def get_public_storage():
    if settings.USE_S3:
        return PublicMediaStorage()
    return FileSystemStorage(location=settings.MEDIA_ROOT / "public")


def get_private_storage():
    if settings.USE_S3:
        return PrivateMediaStorage()
    return FileSystemStorage(location=settings.MEDIA_ROOT / "private")
