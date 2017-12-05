# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantityindisplay',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='store_number',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='tote',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
