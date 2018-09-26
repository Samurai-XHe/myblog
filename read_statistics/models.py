from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.db.models.fields import exceptions


class ReadCount(models.Model):
    read_count = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class GetReadCount:
    def get_read_count(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readcount = ReadCount.objects.get(content_type=ct, object_id=self.pk)
            return readcount.read_count
        except exceptions.ObjectDoesNotExist as e:
            return 0

    def get_one_day_read_count(self):
        today = timezone.now().date()
        try:
            ct = ContentType.objects.get_for_model(self)
            readcount = OneDayReadCount.objects.get(content_type=ct, object_id=self.pk, date=today)
            return readcount.one_day_read_count
        except exceptions.ObjectDoesNotExist as e:
            return 0


class OneDayReadCount(models.Model):
    one_day_read_count = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


