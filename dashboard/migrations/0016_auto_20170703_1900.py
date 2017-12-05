# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_remove_product_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Conversion',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='primary_stock',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
