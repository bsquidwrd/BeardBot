# Generated by Django 2.2.2 on 2019-08-16 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bearddb', '0004_beardlog_event_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='beardlog',
            name='asks',
            field=models.IntegerField(default=0),
        ),
    ]
