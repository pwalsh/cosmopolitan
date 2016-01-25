# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CosmopolitanContinent',
            fields=[
                ('id', models.CharField(serialize=False, max_length=2, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('geoNameId', models.PositiveIntegerField()),
            ],
        ),
    ]
