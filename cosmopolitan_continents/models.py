from django.db import models


class CosmopolitanContinent(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    geoNameId = models.PositiveIntegerField(blank=False)
    countries = models.ManyToManyField('cosmopolitan_countries.CosmopolitanCountry', related_name='related_continent_country')
    currencies = models.ManyToManyField('cosmopolitan_currencies.CosmopolitanCurrency')
