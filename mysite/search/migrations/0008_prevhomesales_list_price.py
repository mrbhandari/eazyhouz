# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0007_remove_prevhomesales_list_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='prevhomesales',
            name='list_price',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
