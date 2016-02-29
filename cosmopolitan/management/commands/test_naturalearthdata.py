from unittest import TestCase

from mock import patch
from mock import MagicMock

from cosmopolitan.management.commands._naturalearthdata import \
    process_countries
from cosmopolitan.management.commands._naturalearthdata import \
    process_cities
from cosmopolitan.management.commands._naturalearthdata import \
    process_regions

mock_country_data = {"features": [
    {"properties":
        {"ISO_A2": "ru"},
        "geometry":
            {"coordinates": "12"}}]}

mock_city_data = {"features": [
    {"properties":
        {"GN_ASCII": "City Name"},
        "geometry":
            {"coordinates": "12"}}]}

mock_region_data = {"features": [
    {"properties":
        {"name": "Region Name"},
        "geometry":
            {"coordinates": "12"}}]}


class ImportTest(TestCase):

    @patch('cosmopolitan.management.commands._naturalearthdata.prepare_data',
           lambda a: mock_country_data)
    @patch('cosmopolitan.management.commands._naturalearthdata.Country')
    @patch('cosmopolitan.management.commands._naturalearthdata.Polygon')
    def test_process_countries(self, Country, Polygon):
        Country.objects = MagicMock()
        process_countries()

    @patch('cosmopolitan.management.commands._naturalearthdata.prepare_data',
           lambda a: mock_city_data)
    @patch('cosmopolitan.management.commands._naturalearthdata.City')
    @patch('cosmopolitan.management.commands._naturalearthdata.Polygon')
    def test_process_cities(self, City, Polygon):
        City.objects = MagicMock()
        process_cities()

    @patch('cosmopolitan.management.commands._naturalearthdata.prepare_data',
           lambda a: mock_region_data)
    @patch('cosmopolitan.management.commands._naturalearthdata.Region')
    @patch('cosmopolitan.management.commands._naturalearthdata.Polygon')
    def test_process_regions(self, Region, Polygon):
        Region.objects = MagicMock()
        process_regions()
