# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_url', models.CharField(unique=True, max_length=400)),
                ('thumbnail_url', models.CharField(unique=True, max_length=400)),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
                ('likes', models.SmallIntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(to='feed.Venue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
