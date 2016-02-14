import factory
from factory.fuzzy import FuzzyText

from django.contrib.gis.geos import GEOSGeometry

from .models import Continent
from .models import Currency
from .models import Country
from .models import City
from .models import Postcode
from .models import Region
from .models import Polygon


class ContinentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Continent

    id = FuzzyText(length=2)
    name = FuzzyText(length=6)
    geoNameId = 12


class CurrencyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Currency

    id = FuzzyText(length=2)
    name = FuzzyText(length=6)


class CountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Country

    id = FuzzyText(length=2)
    population = 2
    continent = factory.SubFactory(ContinentFactory)
    currency = factory.SubFactory(CurrencyFactory)


class CityFactory(factory.DjangoModelFactory):
    class Meta:
        model = City

    id = FuzzyText(length=2)
    name = FuzzyText(length=6)
    location = GEOSGeometry('POINT(5 23)')
    population = 1
    country = factory.SubFactory(CountryFactory)


class RegionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Region

    id = FuzzyText(length=2)
    name = FuzzyText(length=4)
    country = factory.SubFactory(CountryFactory)


class PostcodeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Postcode

    id = FuzzyText(length=2)
    location = GEOSGeometry('POINT(5 23)')
    country = factory.SubFactory(CountryFactory)
    region = factory.SubFactory(RegionFactory)


class PolygonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Polygon

    id = FuzzyText(length=6)
