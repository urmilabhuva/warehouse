# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_product_ingredienttoproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_ingredient',
            field=models.CharField(default=b'No', max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='updatecost',
            field=models.CharField(default=b'Yes', max_length=200),
        ),
    ]
