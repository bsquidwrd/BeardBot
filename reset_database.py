import web.wsgi
from bearddb.models import BeardLog

BeardLog.objects.all().delete()
