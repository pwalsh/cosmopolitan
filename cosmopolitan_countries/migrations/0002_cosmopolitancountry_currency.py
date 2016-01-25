# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmopolitan_currencies', '0001_initial'),
        ('cosmopolitan_countries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cosmopolitancountry',
            name='currency',
            field=models.ForeignKey(null=True, to='cosmopolitan_currencies.CosmopolitanCurrency'),
        ),
    ]
