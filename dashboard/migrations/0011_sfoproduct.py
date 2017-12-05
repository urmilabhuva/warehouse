# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0010_auto_20170624_0631'),
    ]

    operations = [
        migrations.CreateModel(
            name='SFOProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sid', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('barcode', models.CharField(max_length=255, null=True, blank=True)),
                ('sku', models.CharField(max_length=255, null=True, blank=True)),
                ('bin', models.CharField(max_length=255, null=True, blank=True)),
                ('primary_vendor', models.CharField(max_length=255, null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('export_unit', models.CharField(max_length=255, null=True, blank=True)),
                ('threshold', models.DecimalField(default=0, null=True, max_digits=8, decimal_places=5, blank=True)),
                ('quantityinhand', models.DecimalField(default=0, null=True, max_digits=8, decimal_places=5, blank=True)),
                ('quantityinlayaway', models.CharField(max_length=255, null=True, blank=True)),
                ('quantityforsale', models.DecimalField(default=0, null=True, max_digits=8, decimal_places=2, blank=True)),
                ('currentcost', models.DecimalField(default=0, null=True, max_digits=8, decimal_places=2, blank=True)),
                ('totalvalue', models.DecimalField(default=0, null=True, max_digits=8, decimal_places=2, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SFOProduct',
            },
        ),
    ]
