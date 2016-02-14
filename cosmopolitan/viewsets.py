from rest_framework import viewsets
from rest_framework.response import Response

from cosmopolitan import mixins

from .models import Continent
from .models import Currency
from .models import Country
from .models import City
from .models import Region
from .models import Postcode
from .models import Polygon

from .serializers.specific import ContinentListSerializer
from .serializers.specific import ContinentDetailSerializer

from .serializers.specific import CountryListSerializer
from .serializers.specific import CountryDetailSerializer

from .serializers.specific import RegionListSerializer
from .serializers.specific import RegionDetailSerializer

from .serializers.specific import CityListSerializer
from .serializers.specific import CityDetailSerializer

from .serializers.specific import CurrencyListSerializer
from .serializers.specific import CurrencyDetailSerializer

from .serializers.specific import PostcodeListSerializer
from .serializers.specific import PostcodeDetailSerializer

from .serializers.specific import PolygonListSerializer
from .serializers.specific import PolygonDetailSerializer


class CityViewSet(mixins.ListDetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    model = City
    list_serializer = CityListSerializer
    detail_serializer = CityDetailSerializer

    def get_queryset(self):
        queryset = City.objects.all()
        countries = self.request.query_params.get('countries', None)

        if countries is not None:
            countries = countries.split(',')
            queryset = queryset.filter(country_id__in=countries)
        return queryset


class ContinentViewSet(mixins.ListDetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    model = Continent
    queryset = Continent.objects.all()
    list_serializer = ContinentListSerializer
    detail_serializer = ContinentDetailSerializer


class CurrencyViewSet(mixins.ListDetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    model = Currency
    list_serializer = CurrencyListSerializer
    detail_serializer = CurrencyDetailSerializer

    def get_queryset(self):
        queryset = Currency.objects.all()
        countries = self.request.query_params.get('countries', None)

        if countries is not None:
            countries = countries.split(',')
            queryset = queryset.filter(country_id__in=countries)
        return queryset


class RegionViewSet(mixins.ListDetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    model = Region
    list_serializer = RegionListSerializer
    detail_serializer = RegionDetailSerializer

    def get_queryset(self):
        queryset = Region.objects.all()
        countries = self.request.query_params.get('countries', None)
        if countries is not None:
            countries = countries.split(',')
            queryset = queryset.filter(country_id__in=countries)
        return queryset


class PostcodeViewSet(mixins.ListDetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    model = Postcode
    list_serializer = PostcodeListSerializer
    detail_serializer = PostcodeDetailSerializer

    def get_queryset(self):
        queryset = Postcode.objects.all()
        countries = self.request.query_params.get('countries', None)
        if countries is not None:
            countries = countries.split(',')
            queryset = queryset.filter(country_id__in=countries)
        return queryset


class CountryViewSet(mixins.ListDetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    model = Country
    list_serializer = CountryListSerializer
    detail_serializer = CountryDetailSerializer

    def get_queryset(self):
        queryset = Country.objects.all()
        continents = self.request.query_params.get('continents', None)
        if continents is not None:
            continents = continents.split(',')
            queryset = queryset.filter(continent_id__in=continents)
        return queryset

    # TODO: need to find better way of removing self from response
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CountryDetailSerializer(instance,
                                             context={'request': request})
        data = self._remove_self_from_related(serializer.data, request)
        return Response(data)

    def _remove_self_from_related(self, data, request):
        # remove retreived country from list of related Countries
        # to not show it twice
        for idx, current_country in enumerate(data['continent']['related']):
            request_country_code = request.path[-3:-1]
            if current_country['id'] == request_country_code:
                del(data['continent']['related'][idx])
        return data


class PolygonViewSet(mixins.ListDetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    model = Polygon
    queryset = Polygon.objects.all()
    list_serializer = PolygonListSerializer
    detail_serializer = PolygonDetailSerializer
