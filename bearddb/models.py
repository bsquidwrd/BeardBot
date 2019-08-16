from django.db import models


class BeardLog(models.Model):
    event_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    event_user = models.CharField(max_length=255, blank=True, null=True)
    event_type = models.CharField(max_length=255, blank=True, null=True)
    event_points = models.IntegerField(default=0, blank=True, null=True)
    event_team = models.CharField(max_length=10, blank=True, null=True)
    event_message = models.TextField(blank=True, null=True)
    event_test = models.BooleanField(default=True)
    asks = models.IntegerField(default=0)
