# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20141018_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prevhomesales',
            name='baths',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='days_on_market',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='favorite',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='interested',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='is_short_sale',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='last_sale_date',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='last_sale_price',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='listing_id',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='location',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='lot_size',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='next_open_house_date',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='next_open_house_end_time',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='next_open_house_start_time',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='original_list_price',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='original_source',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='parking_spots',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='parking_type',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='recent_reduction_date',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='source',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='sqft',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='status',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='url',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='year_built',
        ),
    ]
