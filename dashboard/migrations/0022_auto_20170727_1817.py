# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_auto_20170727_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sfoproduct',
            name='quantityforsale',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sfoproduct',
            name='threshold',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
