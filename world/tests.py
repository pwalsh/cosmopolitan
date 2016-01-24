from rest_assured.testcases import BaseRESTAPITestCase
from rest_assured.testcases import ListAPITestCaseMixin

from .factory_boys import CosmopolitanCountryFactory
from .factory_boys import ContinentFactory
from .factory_boys import CurrencyFactory


class CountriesTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'cosmopolitancountry'
    factory_class = CosmopolitanCountryFactory


class ContinentTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'cosmopolitancontinent'
    factory_class = ContinentFactory


class CurrencyTest(BaseRESTAPITestCase, ListAPITestCaseMixin):
    base_name = 'cosmopolitancurrency'
    factory_class = CurrencyFactory
