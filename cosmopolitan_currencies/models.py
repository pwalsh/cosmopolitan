from django.db import models


class CosmopolitanCurrency(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    countries = models.ManyToManyField('cosmopolitan_countries.CosmopolitanCountry', related_name='related_country')
    continents = models.ManyToManyField('cosmopolitan_continents.CosmopolitanContinent')
