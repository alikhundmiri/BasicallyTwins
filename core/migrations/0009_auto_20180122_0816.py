# Generated by Django 2.0.1 on 2018-01-22 08:16

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180122_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='adverts',
            name='ad_words',
            field=models.CharField(blank=True, default=0, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='adverts',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='adverts',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=core.models.upload_location, width_field='width_field'),
        ),
        migrations.AddField(
            model_name='adverts',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
    ]
