from rest_framework import viewsets
from rest_framework.response import Response

from cosmopolitan import mixins

from cosmopolitan.models import Continent
from cosmopolitan.models import Currency
from cosmopolitan.models import Country
from cosmopolitan.models import City
from cosmopolitan.models import Region
from cosmopolitan.models import Postcode
from cosmopolitan.models import Polygon

from cosmopolitan.serializers.specific import ContinentListSerializer
from cosmopolitan.serializers.specific import ContinentDetailSerializer

from cosmopolitan.serializers.specific import CountryListSerializer
from cosmopolitan.serializers.specific import CountryDetailSerializer

from cosmopolitan.serializers.specific import RegionListSerializer
from cosmopolitan.serializers.specific import RegionDetailSerializer

from cosmopolitan.serializers.specific import CityListSerializer
from cosmopolitan.serializers.specific import CityDetailSerializer

from cosmopolitan.serializers.specific import CurrencyListSerializer
from cosmopolitan.serializers.specific import CurrencyDetailSerializer

from cosmopolitan.serializers.specific import PostcodeListSerializer
from cosmopolitan.serializers.specific import PostcodeDetailSerializer

from cosmopolitan.serializers.specific import CountryPolygonListSerializer
from cosmopolitan.serializers.specific import CountryPolygonDetailSerializer

from cosmopolitan.serializers.specific import CityPolygonListSerializer
from cosmopolitan.serializers.specific import CityPolygonDetailSerializer

from cosmopolitan.serializers.specific import RegionPolygonListSerializer
from cosmopolitan.serializers.specific import RegionPolygonDetailSerializer

from cosmopolitan.serializers.specific import PolygonListSerializer
from cosmopolitan.serializers.specific import PolygonDetailSerializer


class CityViewSet(mixins.ListDetailSerializerMixin,
                  viewsets.ReadOnlyModelViewSet):
    model = City
    list_serializer = CityListSerializer
    detail_serializer = CityDetailSerializer

    def get_queryset(self):
        queryset = City.objects.all()
        continents = self.request.query_params.get('continents', None)
        regions = self.request.query_params.get('regions', None)
        countries = self.request.query_params.get('countries', None)
        slugs = self.request.query_params.get('slugs', None)

        if slugs is not None:
            slugs = slugs.split(',')
            queryset = queryset.filter(slug__in=slugs)

        if countries is not None:
            countries = countries.split(',')
            queryset = queryset.filter(country_id__in=countries)

        if regions is not None:
            regions = regions.split(',')
            queryset = queryset.filter(region_id__in=regions)

        if continents is not None:
            continents = continents.split(',')
            queryset = queryset.filter(continent_id__in=continents)

        return queryset



class ContinentViewSet(mixins.ListDetailSerializerMixin,
                       viewsets.ReadOnlyModelViewSet):
    model = Continent
    queryset = Continent.objects.all()
    list_serializer = ContinentListSerializer
    detail_serializer = ContinentDetailSerializer


class CurrencyViewSet(mixins.ListDetailSerializerMixin,
                      viewsets.ReadOnlyModelViewSet):
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


class RegionViewSet(mixins.ListDetailSerializerMixin,
                    viewsets.ReadOnlyModelViewSet):
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


class PostcodeViewSet(mixins.ListDetailSerializerMixin,
                      viewsets.ReadOnlyModelViewSet):
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


class CountryViewSet(mixins.ListDetailSerializerMixin,
                     viewsets.ReadOnlyModelViewSet):
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
                del data['continent']['related'][idx]
        return data


class CountryPolygonViewSet(mixins.ListDetailSerializerMixin,
                            viewsets.ReadOnlyModelViewSet):
    model = Polygon
    list_serializer = CountryPolygonListSerializer
    detail_serializer = CountryPolygonDetailSerializer

    def get_queryset(self):
        queryset = Polygon.objects.filter(type='country')
        countries = self.request.query_params.get('countries', None)
        continents = self.request.query_params.get('continents', None)

        if countries is not None:
            countries = countries.split(',')
            queryset = queryset.filter(type_id__in=countries)

        if continents is not None:
            continents = continents.split(',')
            country_list = Country.objects.filter(continent_id__in=continents)
            country_list = [country.id for country in country_list]
            queryset = queryset.filter(type_id__in=country_list)

        return queryset


class CityPolygonViewSet(mixins.ListDetailSerializerMixin,
                         viewsets.ReadOnlyModelViewSet):
    model = Polygon
    list_serializer = CityPolygonListSerializer
    detail_serializer = CityPolygonDetailSerializer

    def get_queryset(self):
        return Polygon.objects.filter(type="city")


class RegionPolygonViewSet(mixins.ListDetailSerializerMixin,
                           viewsets.ReadOnlyModelViewSet):
    model = Polygon
    list_serializer = RegionPolygonListSerializer
    detail_serializer = RegionPolygonDetailSerializer

    def get_queryset(self):
        return Polygon.objects.filter(type="region")


class PolygonViewSet(mixins.ListDetailSerializerMixin,
                     viewsets.ReadOnlyModelViewSet):
    model = Polygon
    list_serializer = PolygonListSerializer
    detail_serializer = PolygonDetailSerializer

    def get_queryset(self):
        queryset = Polygon.objects.all()
        countries = self.request.query_params.get('countries', None)
        continents = self.request.query_params.get('continents', None)

        if countries is not None:
            countries = countries.split(',')
            queryset = queryset.filter(type_id__in=countries)

        if continents is not None:
            continents = continents.split(',')
            country_list = Country.objects.filter(continent_id__in=continents)
            country_list = [country.id for country in country_list]
            queryset = queryset.filter(type_id__in=country_list)

        return queryset
