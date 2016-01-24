from django.db import models


class CosmopolitanCountry(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=200, db_index=True, verbose_name="ascii name")
    slug = models.CharField(max_length=200)
    population = models.IntegerField()
    code3 = models.CharField(max_length=3)
    currency = models.ForeignKey('cosmopolitan_currencies.CosmopolitanCurrency', null=True)
    continent = models.ForeignKey('cosmopolitan_continents.CosmopolitanContinent', null=True)
