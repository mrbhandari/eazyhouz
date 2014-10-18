# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrevHomeSales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sale_type', models.CharField(max_length=500)),
                ('home_type', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=2000)),
                ('city', models.CharField(max_length=2000)),
                ('statecode', models.CharField(max_length=2)),
                ('zipcode', models.IntegerField(null=True)),
                ('list_price', models.IntegerField()),
                ('beds', models.IntegerField()),
                ('baths', models.DecimalField(max_digits=4, decimal_places=1)),
                ('location', models.CharField(max_length=2000)),
                ('sqft', models.IntegerField()),
                ('lot_size', models.IntegerField()),
                ('year_built', models.IntegerField(max_length=4)),
                ('parking_spots', models.IntegerField()),
                ('parking_type', models.CharField(max_length=500)),
                ('days_on_market', models.IntegerField(max_length=4)),
                ('status', models.CharField(max_length=500)),
                ('next_open_house_date', models.DateTimeField()),
                ('next_open_house_start_time', models.DateTimeField()),
                ('next_open_house_end_time', models.DateTimeField()),
                ('recent_reduction_date', models.DateTimeField()),
                ('original_list_price', models.IntegerField()),
                ('last_sale_date', models.DateTimeField()),
                ('last_sale_price', models.IntegerField()),
                ('url', models.URLField()),
                ('source', models.CharField(max_length=500)),
                ('listing_id', models.CharField(max_length=500)),
                ('original_source', models.CharField(max_length=500)),
                ('favorite', models.CharField(max_length=5)),
                ('interested', models.CharField(max_length=5)),
                ('latitude', models.DecimalField(max_digits=15, decimal_places=10)),
                ('longitude', models.DecimalField(max_digits=15, decimal_places=10)),
                ('is_short_sale', models.BooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
