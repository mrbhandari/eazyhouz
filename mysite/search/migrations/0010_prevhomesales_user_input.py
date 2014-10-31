# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0009_auto_20141018_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='prevhomesales',
            name='user_input',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
