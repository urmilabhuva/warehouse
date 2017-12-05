# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=70, unique=True, null=True, blank=True)),
                ('number', models.CharField(max_length=200, null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('userid', models.IntegerField(max_length=15, null=True, blank=True)),
                ('created_by', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Warehouse',
            },
        ),
    ]
