from rest_assured.testcases import BaseRESTAPITestCase
from rest_assured.testcases import ListAPITestCaseMixin

from cosmopolitan.factory_boys import *


class CountriesTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'country'
    factory_class = CountryFactory


class ContinentTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'continent'
    factory_class = ContinentFactory


class CurrencyTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'currency'
    factory_class = CurrencyFactory


class CityTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'city'
    factory_class = CityFactory


class PostcodeTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'postcode'
    factory_class = PostcodeFactory


class RegionTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'region'
    factory_class = RegionFactory


class CityPolygonTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'citypolygon'
    factory_class = CityPolygonFactory


class CountryPolygonTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'countrypolygon'
    factory_class = CountryPolygonFactory


class RegionPolygonTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'regionpolygon'
    factory_class = RegionPolygonFactory
