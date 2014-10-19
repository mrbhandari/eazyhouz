# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0008_prevhomesales_list_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prevhomesales',
            name='list_price',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='sale_type',
        ),
        migrations.RemoveField(
            model_name='prevhomesales',
            name='statecode',
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='baths',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='elementary',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='exterior_rating',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='high',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='image_url',
            field=models.CharField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='interior_rating',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='last_sale_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=15, decimal_places=5, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=15, decimal_places=5, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='lot_size',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='middle',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='remodeled',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='sale_price',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='sqft',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='state',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='url',
            field=models.CharField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='view_rating',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=5, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prevhomesales',
            name='year_built',
            field=models.IntegerField(max_length=4, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='beds',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='city',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='home_type',
            field=models.CharField(max_length=512, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='zipcode',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
