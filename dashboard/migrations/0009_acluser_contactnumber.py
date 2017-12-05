# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_acluser'),
    ]

    operations = [
        migrations.AddField(
            model_name='acluser',
            name='contactnumber',
            field=models.CharField(default=datetime.datetime(2017, 6, 22, 19, 24, 44, 892686, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
    ]
