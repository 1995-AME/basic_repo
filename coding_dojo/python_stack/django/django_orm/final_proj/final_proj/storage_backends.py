from django.conf import settings
from storage_backends.s3boto3 import S3boto3Storage

class MediaStorage(S3Boto3Storage):
	location = settings.MEDIAFILES_LOCATION
	file_overwrite = False