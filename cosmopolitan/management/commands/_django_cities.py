from cities.models import Country as DjangoCitiesCountry
from cities.models import Region as DjangoCitiesRegion
from cities.models import City as DjangoCitiesCity
from cities.models import PostalCode as DjangoCitiesPostcode

from cosmopolitan.models import Continent
from cosmopolitan.models import Country
from cosmopolitan.models import Currency
from cosmopolitan.models import Region
from cosmopolitan.models import City
from cosmopolitan.models import Postcode


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

    Continent.objects.all().delete()

    print("\n--- Seeding continents: ---")

    for continent in continents_data:
        c = Continent(id=continent['id'], name=continent['name'], geoNameId=continent['geoNameId'])
        c.save()
        print(".", end="")

def process_countries():
    Country.objects.all().delete()

    print("\n--- Seeding countries: ---")

    for country in DjangoCitiesCountry.objects.all():
        ex = Country(pk=country.code.lower(),
                     code3=country.code3.lower(),
                     name=country.name,
                     slug=country.slug,
                     population=country.population)
        ex.save()
        print(".", end="")

def process_currencies():
    Currency.objects.all().delete()

    print("\n--- Seeding currencies for countries ---")

    for dc_country in DjangoCitiesCountry.objects.all():
        if (str(dc_country.currency) == '') or (str(dc_country.currency_name) == ''):
            continue
        # trying to find a currency with the same code first
        try:
            currency = Currency.objects.get(pk=dc_country.currency.lower())
        except Currency.DoesNotExist: # no such currency yet
            currency = Currency(pk=dc_country.currency.lower(),
                                name=dc_country.currency_name)
        currency.save()
        country = Country.objects.get(pk=dc_country.code.lower())
        currency.countries.add(country.pk)
        print(".", end="")

def process_relations():
    process_continents_to_countries()
    process_continents_to_currencies()
    process_currencies_to_countries()
    process_countries_to_continents()
    process_currencies_to_continents()

def process_continents_to_countries():
    for country in Country.objects.all():
        if country.continent:
            country.continent.delete()

    print("\n--- Adding continents to countries ---")

    for country in Country.objects.all():
        dc_country = DjangoCitiesCountry.objects.get(code=country.pk.upper())
        continent = Continent.objects.get(pk=dc_country.continent.lower())
        country.continent_id = continent.pk
        country.save()
        print(".", end="")

def process_continents_to_currencies():
    for continent in Continent.objects.all():
        continent.currencies.all().delete()

    print("\n--- Adding continents to currencies ---")

    for currency in Currency.objects.all():
        for country in currency.countries.all():
            continent = country.continent

            if not currency.continents.filter(pk=continent.pk).exists():
                currency.continents.add(continent.pk)
                print(".", end="")

def process_currencies_to_countries():
    for country in Country.objects.all():
        if country.currency:
            country.currency.delete()

    print("\n--- Adding currencies to countries ---")

    for dc_country in DjangoCitiesCountry.objects.all():
        try:
            currency = Currency.objects.get(pk=dc_country.currency.lower())
            country = Country.objects.get(pk=dc_country.code.lower())
            country.currency_id = currency.pk
            country.save()
            print(".", end="")
        except Currency.DoesNotExist:
            pass

def process_currencies_to_continents():
    for continent in Continent.objects.all():
        continent.currencies.all().delete()

    print("\n--- Adding currencies to continents ---")

    for continent in Continent.objects.all():
        for country in continent.countries.all():
            try:
                dc_country = DjangoCitiesCountry.objects.get(code=country.pk.upper())
                currency = Currency.objects.get(pk=dc_country.currency.lower())
                if not continent.currencies.filter(pk=currency.pk).exists():
                    continent.currencies.add(currency.pk)
                    print(".", end="")
            except Currency.DoesNotExist:
                pass

def process_countries_to_continents():
    for continent in Continent.objects.all():
        continent.countries.all().delete()

    print("\n--- Adding countries to continents ---")

    for continent in Continent.objects.all():
        for country in Country.objects.all():
            if not continent.countries.filter(pk=country.pk).exists():
                if country.continent.pk == continent.pk:
                    continent.countries.add(country.pk)
                    print(".", end="")

def process_regions():
    Region.objects.all().delete()

    print("\n--- Seeding regions ---")

    for dc_region in DjangoCitiesRegion.objects.all():
        country = Country.objects.get(pk=dc_region.country.code.lower())
        region = Region(id=dc_region.code.lower(),
                        name=dc_region.name,
                        name_std=dc_region.name_std,
                        country=country)
        region.save()
        print(".", end="")

def process_cities():
    City.objects.all().delete()

    print("\n--- Seeding cities ---")

    for dc_city in DjangoCitiesCity.objects.all():
        try:
            region = Region.objects.get(pk=dc_city.region.code.lower())
        except AttributeError:
            region = None
        try:
            country = Country.objects.get(pk=dc_city.country.code.lower())
        except AttributeError:
            country = None
        # one city with name Ak”yar has no slug, so we set it here
        if dc_city.slug == '':
            dc_city.slug = 'aky'
        city = City(id=dc_city.id,
                    slug=dc_city.slug.lower(),
                    name=dc_city.name,
                    name_std=dc_city.name_std,
                    location=dc_city.location,
                    population=dc_city.population,
                    region=region,
                    country=country,
                    elevation=dc_city.elevation,
                    kind=dc_city.kind,
                    timezone=dc_city.timezone)
        city.save()
        print(".", end="")

def process_postcodes():
    Postcode.objects.all().delete()

    print("\n--- Seeding postcodes ---")

    for dc_postcode in DjangoCitiesPostcode.objects.all():
        country = Country.objects.get(pk=dc_postcode.country.code.lower())
        postcode = Postcode(id=dc_postcode.code.lower(),
                            location=dc_postcode.location,
                            country=country,
                            region_name=dc_postcode.region_name,
                            subregion_name=dc_postcode.subregion_name,
                            district_name=dc_postcode.district_name)
        postcode.save()
        print(".", end="", flush=True)

def add_regions_to_postcodes():
    for postcode in Postcode.objects.all():
        if postcode.region:
            postcode.region.delete()

    print("\n--- Seeding regions to postcodes ---", flush=True)

    for postcode in Postcode.objects.all():
        region = Region.objects.filter(name=postcode.region_name).first()
        if region:
            postcode.region = region
            postcode.save()
            print(".", end="", flush=True)
