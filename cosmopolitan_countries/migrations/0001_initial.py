# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmopolitan_continents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CosmopolitanCountry',
            fields=[
                ('id', models.CharField(serialize=False, max_length=2, primary_key=True)),
                ('name', models.CharField(verbose_name='ascii name', db_index=True, max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('population', models.IntegerField()),
                ('code3', models.CharField(max_length=3)),
                ('continent', models.ForeignKey(null=True, to='cosmopolitan_continents.CosmopolitanContinent')),
            ],
        ),
    ]
