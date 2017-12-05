# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_auto_20170725_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sfoproduct',
            name='quantityinhand',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
