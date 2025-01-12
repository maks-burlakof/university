from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    use_ssl = True
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "private"
    use_ssl = True
    file_overwrite = False
    custom_domain = False
