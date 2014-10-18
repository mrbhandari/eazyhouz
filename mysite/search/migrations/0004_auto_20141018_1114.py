# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20141018_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prevhomesales',
            name='next_open_house_end_time',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='prevhomesales',
            name='next_open_house_start_time',
            field=models.CharField(max_length=50),
        ),
    ]
