# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_auto_20141018_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prevhomesales',
            name='list_price',
        ),
    ]
