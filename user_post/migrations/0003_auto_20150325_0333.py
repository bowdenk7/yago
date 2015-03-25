# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_post', '0002_reportedpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(related_name='likes', to='user_post.Post'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='venue',
            field=models.ForeignKey(related_name='venues', to='feed.Venue'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reportedpost',
            name='post',
            field=models.ForeignKey(related_name='reported_posts', to='user_post.Post'),
            preserve_default=True,
        ),
    ]
