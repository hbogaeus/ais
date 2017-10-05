from django.contrib.auth.models import Permission
from banquet.models import BanquetteAttendant
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(BanquetteAttendant)
Permission.objects.create(content_type=content_type, codename='banquet_full_permission')
