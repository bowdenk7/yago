# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('expiration', models.DateTimeField(blank=True)),
                ('redeemed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PromotionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=400)),
                ('point_cost', models.IntegerField()),
                ('venue', models.ForeignKey(to='feed.Venue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='promotion',
            name='type',
            field=models.ForeignKey(to='promotion.PromotionType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='promotion',
            name='user',
            field=models.ForeignKey(related_name='promotions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
