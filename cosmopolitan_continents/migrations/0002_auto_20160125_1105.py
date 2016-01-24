# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmopolitan_currencies', '0001_initial'),
        ('cosmopolitan_continents', '0001_initial'),
        ('cosmopolitan_countries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cosmopolitancontinent',
            name='countries',
            field=models.ManyToManyField(to='cosmopolitan_countries.CosmopolitanCountry', related_name='related_continent_country'),
        ),
        migrations.AddField(
            model_name='cosmopolitancontinent',
            name='currencies',
            field=models.ManyToManyField(to='cosmopolitan_currencies.CosmopolitanCurrency'),
        ),
    ]
