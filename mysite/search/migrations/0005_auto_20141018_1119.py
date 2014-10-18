# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20141018_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prevhomesales',
            name='address',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='baths',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='beds',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='city',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='days_on_market',
            field=models.IntegerField(max_length=4, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='favorite',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='home_type',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='interested',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='last_sale_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='last_sale_price',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=15, decimal_places=10, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='list_price',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='listing_id',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='location',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=15, decimal_places=10, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='lot_size',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='next_open_house_date',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='next_open_house_end_time',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='next_open_house_start_time',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='original_list_price',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='original_source',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='parking_spots',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='parking_type',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='recent_reduction_date',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='sale_type',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='source',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='sqft',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='statecode',
            field=models.CharField(max_length=2, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='status',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='year_built',
            field=models.IntegerField(max_length=4, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='zipcode',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
    ]
