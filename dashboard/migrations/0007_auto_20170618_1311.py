# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20170618_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bin_location',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
