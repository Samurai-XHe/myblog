from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadCount,OneDayReadCount

def add_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' %(ct.model,obj.pk)

    if not request.COOKIES.get(key):
        # 总阅读数+1
        readcount,xx = ReadCount.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readcount.read_count += 1
        readcount.save()

        #当天阅读数+1
        date = timezone.now().date()
        onedayreadcount,xx = OneDayReadCount.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        onedayreadcount.one_day_read_count += 1
        onedayreadcount.save()
    return key


