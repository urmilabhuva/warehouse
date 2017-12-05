# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20170627_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='sfoproduct',
            name='reorder_unit',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
