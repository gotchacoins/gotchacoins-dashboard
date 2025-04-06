from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    location = getattr(settings, "AWS_PRIVATE_MEDIA_LOCATION", "media/private")
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
