from rest_framework import serializers
from cities.models import Country
from .models import CosmopolitanCountry

from cosmopolitan_currencies.models import CosmopolitanCurrency
from cosmopolitan_continents.models import CosmopolitanContinent


class CountryShortSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CosmopolitanCountry
        fields = ('url', 'id')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CosmopolitanCountry
        fields = ('url', 'id', 'name')

###
# Currencies
###

class CurrencyShortCountrySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.StringRelatedField()
    countries = CountryShortSerializer(many=True, read_only=True)

    class Meta:
        model = CosmopolitanCurrency
        exclude = ('continents',)


class ContinentCurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CosmopolitanContinent
        fields = ('url', 'name', 'id')


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.StringRelatedField()
    countries = CountrySerializer(many=True, read_only=True)
    continents = ContinentCurrencySerializer(many=True, read_only=True)

    class Meta:
        model = CosmopolitanCurrency


class CurrencyShortSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CosmopolitanCurrency
        fields = ('name', 'id', 'url')


###
# Continents
###

class ContinentCountrySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.StringRelatedField()
    name = serializers.StringRelatedField()
    related = CountryShortSerializer(many=True, read_only=True, source='countries')

    class Meta:
        model = CosmopolitanContinent
        exclude = ('countries', 'geoNameId', 'currencies')


class ContinentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.StringRelatedField()
    countries = CountryShortSerializer(many=True, read_only=True)

    class Meta:
        model = CosmopolitanContinent
        exclude = ('currencies',)


class ContinentShortSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CosmopolitanContinent
        fields = ('url', 'id')


class ContinentDetailedSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.StringRelatedField()
    countries = CountrySerializer(many=True, read_only=True)
    currencies = CurrencyShortSerializer(many=True, read_only=True)

    class Meta:
        model = CosmopolitanContinent


###
# Countries
###
class CosmopolitanCountrySerializer(serializers.HyperlinkedModelSerializer):
    continent = ContinentCountrySerializer()
    currency = CurrencyShortSerializer()

    class Meta:
        model = CosmopolitanCountry
        fields = ('id', 'url', 'name', 'continent', 'currency')


class CosmopolitanCountryShortSerializer(CosmopolitanCountrySerializer):
    continent = ContinentShortSerializer()
