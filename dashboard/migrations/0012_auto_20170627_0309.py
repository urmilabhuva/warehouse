# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_sfoproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sfoproduct',
            name='currentcost',
            field=models.DecimalField(default=0, null=True, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='sfoproduct',
            name='quantityforsale',
            field=models.DecimalField(default=0, null=True, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='sfoproduct',
            name='quantityinhand',
            field=models.DecimalField(default=0, null=True, max_digits=11, decimal_places=5, blank=True),
        ),
        migrations.AlterField(
            model_name='sfoproduct',
            name='threshold',
            field=models.DecimalField(default=0, null=True, max_digits=11, decimal_places=5, blank=True),
        ),
        migrations.AlterField(
            model_name='sfoproduct',
            name='totalvalue',
            field=models.DecimalField(default=0, null=True, max_digits=11, decimal_places=2, blank=True),
        ),
    ]
