import factory
from factory.fuzzy import FuzzyText

from django.contrib.gis.geos import GEOSGeometry

from cosmopolitan_continents.models import CosmopolitanContinent
from cosmopolitan_currencies.models import CosmopolitanCurrency
from cosmopolitan_countries.models import CosmopolitanCountry

from cities.models import Country
from cities.models import Region
from cities.models import City


class CountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Country

    name = FuzzyText(length=6)
    population = 1


class RegionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Region

    name = FuzzyText(length=6)
    country = factory.SubFactory(CountryFactory)


class CityFactory(factory.DjangoModelFactory):
    class Meta:
        model = City

    name = FuzzyText(length=6)
    location = GEOSGeometry('POINT(5 23)')
    population = 1
    country = factory.SubFactory(CountryFactory)
    region = factory.SubFactory(RegionFactory)


class ContinentFactory(factory.DjangoModelFactory):
    class Meta:
        model = CosmopolitanContinent

    id = FuzzyText(length=2)
    name = FuzzyText(length=6)
    geoNameId = 12


class CurrencyFactory(factory.DjangoModelFactory):
    class Meta:
        model = CosmopolitanCurrency

    id = FuzzyText(length=2)
    name = FuzzyText(length=6)


class CosmopolitanCountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = CosmopolitanCountry

    id = FuzzyText(length=2)
    continent = factory.SubFactory(ContinentFactory)
    currency = factory.SubFactory(CurrencyFactory)
    population = 1
