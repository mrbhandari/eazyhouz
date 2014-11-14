# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeadGenUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=512)),
                ('email_address', models.EmailField(max_length=512)),
                ('inquiry_reason', models.CharField(default=b'Select', max_length=1024)),
                ('property_address', models.CharField(max_length=1024, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=10, null=True)),
                ('user_agent', models.CharField(max_length=1024, null=True, blank=True)),
                ('remote_address', models.IPAddressField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now=True, null=True)),
                ('zestimate_found', models.NullBooleanField()),
                ('zestimate_link', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrevHomeSales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('home_type', models.CharField(max_length=512, null=True, blank=True)),
                ('address', models.CharField(max_length=2000, null=True, blank=True)),
                ('city', models.CharField(max_length=500, null=True, blank=True)),
                ('state', models.CharField(max_length=50, null=True, blank=True)),
                ('zipcode', models.CharField(max_length=10, null=True, blank=True)),
                ('sale_price', models.IntegerField(null=True, blank=True)),
                ('beds', models.IntegerField(null=True, blank=True)),
                ('baths', models.DecimalField(null=True, max_digits=4, decimal_places=1, blank=True)),
                ('sqft', models.IntegerField(null=True, blank=True)),
                ('lot_size', models.IntegerField(null=True, blank=True)),
                ('year_built', models.IntegerField(max_length=4, null=True, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=15, decimal_places=9, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=15, decimal_places=9, blank=True)),
                ('interior_rating', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('exterior_rating', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('view_rating', models.DecimalField(null=True, max_digits=5, decimal_places=5, blank=True)),
                ('url', models.CharField(max_length=2000, null=True, blank=True)),
                ('image_url', models.CharField(max_length=2000, null=True, blank=True)),
                ('elementary', models.IntegerField(null=True, blank=True)),
                ('middle', models.IntegerField(null=True, blank=True)),
                ('high', models.IntegerField(null=True, blank=True)),
                ('remodeled', models.NullBooleanField()),
                ('last_sale_date', models.DateField(null=True, blank=True)),
                ('user_input', models.NullBooleanField()),
                ('last_zestimate', models.IntegerField(null=True, blank=True)),
                ('curr_status', models.CharField(max_length=512, null=True, blank=True)),
                ('property_type', models.CharField(max_length=512, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
