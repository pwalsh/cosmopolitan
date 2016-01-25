from __future__ import print_function

from optparse import make_option

from django.core.management.base import BaseCommand

from cities.models import Country

from cosmopolitan_continents.models import CosmopolitanContinent
from cosmopolitan_countries.models import CosmopolitanCountry
from cosmopolitan_currencies.models import CosmopolitanCurrency

# more stuff could be added here
IMPORT_OPTS = [
    "all",
    "django_cities",
]

def process_continents():
    continents_data = [
        {'id': 'af', 'name': 'Africa', 'geoNameId': 6255146},
        {'id': 'as', 'name': 'Asia', 'geoNameId': 6255147},
        {'id': 'eu', 'name': 'Europe', 'geoNameId': 6255148},
        {'id': 'na', 'name': 'North America', 'geoNameId': 6255149},
        {'id': 'oc', 'name': 'Oceania', 'geoNameId': 6255151},
        {'id': 'sa', 'name': 'South America', 'geoNameId': 6255150},
        {'id': 'an', 'name': 'Antarctica', 'geoNameId': 6255152},
    ]

    CosmopolitanContinent.objects.all().delete()

    print("\n--- Seeding continents: ---")
    for continent in continents_data:
        c = CosmopolitanContinent(id=continent['id'], name=continent['name'], geoNameId=continent['geoNameId'])
        c.save()
        print(".", end="")

def process_countries():
    CosmopolitanCountry.objects.all().delete()
    print("\n--- Seeding countries: ---")
    for country in Country.objects.all():
        ex = CosmopolitanCountry(pk=country.code.lower(),
                          code3=country.code3.lower(),
                          name=country.name,
                          slug=country.slug,
                          population=country.population)
        ex.save()
        print(".", end="")

def process_currencies():
    CosmopolitanCurrency.objects.all().delete()

    print("\n--- Seeding currencies for countries ---")
    for country in Country.objects.all():
        # trying to find a currency with the same code first
        try:
            currency = CosmopolitanCurrency.objects.get(pk=country.currency.lower())
        except CosmopolitanCurrency.DoesNotExist: # no such currency yet
            currency = CosmopolitanCurrency(pk=country.currency.lower(),
                                            name=country.currency_name)
        if (str(country.currency) == '') or (str(country.currency_name) == ''):
            pass
        else:
            currency.save()
            cosmopolitan_country = CosmopolitanCountry.objects.get(pk=country.code.lower())
            currency.countries.add(cosmopolitan_country.pk)
            print(".", end="")

def process_relations():
    process_continents_to_countries()
    process_continents_to_currencies()
    process_currencies_to_countries()
    process_countries_to_continents()
    process_currencies_to_continents()

def process_continents_to_countries():
    for country in CosmopolitanCountry.objects.all():
        if country.continent:
            country.continent.delete()

    print("\n--- Adding continents to countries ---")

    for cosmopolitan_country in CosmopolitanCountry.objects.all():
        country = Country.objects.get(code=cosmopolitan_country.pk.upper())
        continent = CosmopolitanContinent.objects.get(pk=country.continent.lower())
        cosmopolitan_country.continent_id = continent.pk
        cosmopolitan_country.save()
        print(".", end="")

def process_continents_to_currencies():
    for continent in CosmopolitanContinent.objects.all():
        continent.currencies.all().delete()

    print("\n--- Adding continents to currencies ---")

    for currency in CosmopolitanCurrency.objects.all():
        for cosmopolitan_country in currency.countries.all():
            continent = cosmopolitan_country.continent

            if not currency.continents.filter(pk=continent.pk).exists():
                currency.continents.add(continent.pk)
                print(".", end="")

def process_currencies_to_countries():
    for country in CosmopolitanCountry.objects.all():
        if country.currency:
            country.currency.delete()

    print("\n--- Adding currencies to countries ---")

    for country in Country.objects.all():
        try:
            currency = CosmopolitanCurrency.objects.get(pk=country.currency.lower())
            cosmopolitan_country = CosmopolitanCountry.objects.get(pk=country.code.lower())
            cosmopolitan_country.currency_id = currency.pk
            cosmopolitan_country.save()
            print(".", end="")
        except CosmopolitanCurrency.DoesNotExist:
            pass

def process_currencies_to_continents():
    for continent in CosmopolitanContinent.objects.all():
        continent.currencies.all().delete()

    print("\n--- Adding currencies to continents ---")

    for continent in CosmopolitanContinent.objects.all():
        for cosmopolitan_country in continent.countries.all():
            try:
                country = Country.objects.get(code=cosmopolitan_country.pk.upper())
                currency = CosmopolitanCurrency.objects.get(pk=country.currency.lower())
                if not continent.currencies.filter(pk=currency.pk).exists():
                    continent.currencies.add(currency.pk)
                    print(".", end="")
            except CosmopolitanCurrency.DoesNotExist:
                pass

def process_countries_to_continents():
    for continent in CosmopolitanContinent.objects.all():
        continent.countries.all().delete()

    print("\n--- Adding countries to continents ---")

    for continent in CosmopolitanContinent.objects.all():
        for country in CosmopolitanCountry.objects.all():
            if not continent.countries.filter(pk=country.pk).exists():
                if country.continent.pk == continent.pk:
                    continent.countries.add(country.pk)
                    print(".", end="")



class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--from", metavar="IMPORT_SOURCE", default='all',
                    help="Selectively import data. Comma separated list of import sources: "
                    + str(IMPORT_OPTS).replace("'", "")
                   ),
    )

    def handle(self, *args, **options):
        self.options = options
        self.data_sources = [e for e in self.options["from"].split(",") if e]

        if not set(self.data_sources).issubset(set(IMPORT_OPTS)):
            raise ValueError("Invalid option")

        for data_source in self.data_sources:
            func = getattr(self, "_import_" + data_source)
            func()

    def _import_django_cities(self):
        process_continents()
        process_countries()
        process_currencies()
        process_relations()

    def _import_all(self):
        self._import_django_cities()
        print("\nImport finished")
