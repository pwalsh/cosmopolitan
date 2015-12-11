from rest_framework import viewsets
from rest_framework.response import Response

from cities.models import Region
from cities.models import Subregion
from cities.models import City

from continents.models import Continent
from currencies.models import Currency

from .serializers import RegionSerializer
from .serializers import SubregionSerializer
from .serializers import CitySerializer
from .serializers import ContinentSerializer
from .serializers import CurrencySerializer

from extra_countries.models import ExtraCountry
from extra_countries.serializers import ExtraCountrySerializer
from extra_countries.serializers import ExtraCountrySerializerShort


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    model = Region
    serializer_class = RegionSerializer
    queryset = Region.objects.all()

    def get_queryset(self):
        try:
            country_id = self.kwargs['country_id']
        except KeyError:
            return self.queryset
        return self.queryset.filter(country=country_id)


class SubregionViewSet(viewsets.ReadOnlyModelViewSet):
    model = Subregion
    serializer_class = SubregionSerializer
    queryset = Subregion.objects.all()

    def get_queryset(self):
        try:
            region_id = self.kwargs['region_id']
        except KeyError:
            return self.queryset
        return self.queryset.filter(region=region_id)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    model = City
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get_queryset(self):
        try:
            region_id = self.kwargs['region_id']
        except KeyError:
            return self.queryset
        return self.queryset.filter(region=region_id)


class ContinentViewSet(viewsets.ReadOnlyModelViewSet):
    model = Continent
    serializer_class = ContinentSerializer
    queryset = Continent.objects.all()


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    model = Currency
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


class ExtraCountryViewSet(viewsets.ReadOnlyModelViewSet):
    model = ExtraCountry
    serializer_class = ExtraCountrySerializer
    queryset = ExtraCountry.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ExtraCountrySerializerShort(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def detail(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = ExtraCountrySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
