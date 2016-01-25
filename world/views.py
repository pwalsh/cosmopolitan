from rest_framework import viewsets
from rest_framework.response import Response

from cosmopolitan_continents.models import CosmopolitanContinent
from cosmopolitan_currencies.models import CosmopolitanCurrency

from cosmopolitan_countries.models import CosmopolitanCountry
from cosmopolitan_countries.serializers import CosmopolitanCountrySerializer
from cosmopolitan_countries.serializers import CosmopolitanCountryShortSerializer
from cosmopolitan_countries.serializers import ContinentSerializer
from cosmopolitan_countries.serializers import ContinentDetailedSerializer
from cosmopolitan_countries.serializers import CurrencySerializer
from cosmopolitan_countries.serializers import CurrencyShortCountrySerializer


class ContinentViewSet(viewsets.ReadOnlyModelViewSet):
    model = CosmopolitanContinent
    serializer_class = ContinentSerializer
    queryset = CosmopolitanContinent.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ContinentDetailedSerializer(instance,
                                                 context={'request': request})
        return Response(serializer.data)


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    model = CosmopolitanCurrency
    serializer_class = CurrencySerializer
    queryset = CosmopolitanCurrency.objects.all()

    def get_queryset(self):
        queryset = CosmopolitanCurrency.objects.all()
        countries = self.request.query_params.get('countries', None)

        if countries is not None:
            countries = countries.split(',')
            queryset = queryset.filter(countries__in=countries)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        srializr = CurrencyShortCountrySerializer(queryset,
                                                  many=True,
                                                  context={'request': request})
        return Response(srializr.data)


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    model = CosmopolitanCountry
    serializer_class = CosmopolitanCountrySerializer
    queryset = CosmopolitanCountry.objects.all()

    def get_queryset(self):
        queryset = CosmopolitanCountry.objects.all()
        continents = self.request.query_params.get('continents', None)
        if continents is not None:
            continents = continents.split(',')
            queryset = queryset.filter(continent_id__in=continents)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CosmopolitanCountryShortSerializer(queryset,
                                                        many=True,
                                                        context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CosmopolitanCountrySerializer(instance,
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
