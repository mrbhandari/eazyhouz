# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20141018_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prevhomesales',
            name='next_open_house_date',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='recent_reduction_date',
            field=models.CharField(max_length=50),
        ),
    ]
