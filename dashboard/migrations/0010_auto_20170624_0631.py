# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_acluser_contactnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
