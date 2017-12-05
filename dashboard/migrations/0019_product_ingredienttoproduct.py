# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ingredienttoproduct',
            field=models.CharField(default=b'No', max_length=200),
        ),
    ]
