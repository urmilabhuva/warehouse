# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0004_apikey'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vendor_product_id', models.CharField(max_length=200)),
                ('bin_location', models.CharField(max_length=255)),
                ('product_name', models.CharField(max_length=255, null=True, blank=True)),
                ('barcode_num', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(max_length=10)),
                ('quantityindisplay', models.IntegerField(max_length=50, null=True, blank=True)),
                ('picklist', models.CharField(max_length=255)),
                ('sku', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=255)),
                ('tote', models.IntegerField(max_length=30, null=True, blank=True)),
                ('store_number', models.IntegerField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('store', models.ForeignKey(to='dashboard.Store')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(to='dashboard.Warehouse')),
            ],
            options={
                'db_table': 'Product',
            },
        ),
    ]
