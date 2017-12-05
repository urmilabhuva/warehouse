# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0007_auto_20170618_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acluser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('store', models.ForeignKey(to='dashboard.Store')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(to='dashboard.Warehouse')),
            ],
            options={
                'db_table': 'Acluser',
            },
        ),
    ]
