from cosmopolitan.models import Continent
from cosmopolitan.models import Currency
from cosmopolitan.models import Country
from cosmopolitan.models import City
from cosmopolitan.models import Region
from cosmopolitan.models import Postcode
from cosmopolitan.models import Polygon

from cosmopolitan.serializers.common import CurrencySerializer
from cosmopolitan.serializers.common import CountrySerializer
from cosmopolitan.serializers.common import ContinentSerializer
from cosmopolitan.serializers.common import CitySerializer
from cosmopolitan.serializers.common import RegionSerializer
from cosmopolitan.serializers.common import PostcodeSerializer
from cosmopolitan.serializers.common import PolygonSerializer

from cosmopolitan.serializers.internal import CountryShortSerializer
from cosmopolitan.serializers.internal import ContinentShortSerializer
from cosmopolitan.serializers.internal import CurrencyShortSerializer
from cosmopolitan.serializers.internal import RegionShortSerializer

from cosmopolitan.serializers.internal import ContinentWithRelatedSerializer


class PolygonListSerializer(PolygonSerializer):
    class Meta:
        model = Polygon
        fields = ('id', 'url', 'type', 'type_id')


class PolygonDetailSerializer(PolygonSerializer):
    class Meta:
        model = Polygon
        fields = ('id', 'url', 'type', 'type_id', 'polygon')


class CurrencyListSerializer(CurrencySerializer):
    countries = CountryShortSerializer(many=True, read_only=True)
    class Meta:
        model = Currency
        fields = ('id', 'url', 'name', 'countries')


class CurrencyDetailSerializer(CurrencySerializer):
    countries = CountrySerializer(many=True, read_only=True)
    continents = ContinentSerializer(many=True, read_only=True)
    class Meta:
        model = Currency
        fields = ('id', 'url', 'name', 'countries', 'continents')


class ContinentListSerializer(ContinentSerializer):
    countries = CountryShortSerializer(many=True, read_only=True)
    class Meta:
        model = Continent
        fields = ('id', 'url', 'name', 'countries')


class ContinentDetailSerializer(ContinentSerializer):
    countries = CountrySerializer(many=True, read_only=True)
    currencies = CurrencySerializer(many=True, read_only=True)
    class Meta:
        model = Continent
        fields = ('id', 'url', 'name', 'countries', 'currencies')


class CountryListSerializer(CountrySerializer):
    currency = CurrencyShortSerializer()
    continent = ContinentShortSerializer()

    class Meta:
        model = Country
        fields = ('id', 'url', 'name', 'continent', 'currency')


class CountryDetailSerializer(CountrySerializer):
    currency = CurrencySerializer()
    continent = ContinentWithRelatedSerializer()
    class Meta:
        model = Country
        fields = ('id', 'url', 'name', 'continent', 'currency')


class CityListSerializer(CitySerializer):
    country = CountryShortSerializer()
    region = RegionShortSerializer(allow_null=True)
    class Meta:
        model = City
        fields = ('id', 'url', 'name', 'name_std', 'kind', 'country', 'region')


class CityDetailSerializer(CitySerializer):
    country = CountryShortSerializer()
    region = RegionShortSerializer(allow_null=True)
    class Meta:
        model = City
        fields = ('id', 'url', 'name', 'name_std', 'kind', 'country',
                  'region', 'location', 'population', 'elevation', 'timezone')


class RegionListSerializer(RegionSerializer):
    country = CountryShortSerializer()
    class Meta:
        model = Region
        fields = ('id', 'url', 'name', 'country')


class RegionDetailSerializer(RegionSerializer):
    country = CountrySerializer()
    continent = ContinentSerializer(source='country.continent')
    class Meta:
        model = Region
        fields = ('id', 'url', 'name', 'country', 'continent')


class PostcodeListSerializer(PostcodeSerializer):
    country = CountryShortSerializer()
    region = RegionShortSerializer()
    class Meta:
        model = Postcode
        fields = ('id', 'url', 'country', 'region')


class PostcodeDetailSerializer(PostcodeSerializer):
    country = CountryListSerializer()
    region = RegionSerializer()
    class Meta:
        model = Postcode
        fields = ('id', 'url', 'country', 'region')
