# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmopolitan_continents', '0001_initial'),
        ('cosmopolitan_countries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CosmopolitanCurrency',
            fields=[
                ('id', models.CharField(serialize=False, max_length=3, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('continents', models.ManyToManyField(to='cosmopolitan_continents.CosmopolitanContinent')),
                ('countries', models.ManyToManyField(to='cosmopolitan_countries.CosmopolitanCountry', related_name='related_country')),
            ],
        ),
    ]
