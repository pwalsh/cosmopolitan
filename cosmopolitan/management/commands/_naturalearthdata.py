from __future__ import print_function

import json

from cosmopolitan.models import Country
from cosmopolitan.models import City
from cosmopolitan.models import Region
from cosmopolitan.models import Polygon

from cosmopolitan.management.commands.service.common import prepare_data

# countrise data URL
# http://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip

COUNTRIES = {
    "file_name_without_extension": "ne_10m_admin_0_countries",
    "file_name": "ne_10m_admin_0_countries.zip",
}

CITIES = {
    "file_name_without_extension": "ne_10m_populated_places",
    "file_name": "ne_10m_populated_places.zip",
}


REGIONS = {
    "file_name_without_extension": "ne_10m_admin_1_states_provinces",
    "file_name": "ne_10m_admin_1_states_provinces.zip",
}


def process_countries():
    data = prepare_data(COUNTRIES)

    print("\n--- Seeding countries: ---")

    Polygon.objects.filter(type='country').delete()

    for feature in data["features"]:
        json_country_code = feature["properties"]["ISO_A2"]
        try:
            country = Country.objects.get(pk=json_country_code.lower())
        except Country.DoesNotExist:
            print('Not found: ' + json_country_code, end='')

        polygon = Polygon(id="%s:%s" % ("country", country.id))
        polygon.type = "country"
        polygon.type_id = country.id
        polygon.polygon = json.dumps(feature["geometry"]["coordinates"])
        polygon.save()

        print(".", end="")

    print("\nFinish.")


def process_cities():
    data = prepare_data(CITIES)

    print("\n--- Seeding cities: ---")

    Polygon.objects.filter(type='city').delete()

    for feature in data["features"]:
        json_city_id = int(feature["properties"]["GEONAMEID"])
        try:
            if json_city_id is None:
                continue
            city = City.objects.get(id=str(json_city_id))
            polygon = Polygon(id="%s:%s" % ("city", city.id))
            polygon.type = "city"
            polygon.type_id = city.id
            polygon.polygon = json.dumps(feature["geometry"]["coordinates"])
            polygon.save()
            print(".", end="")
        except City.DoesNotExist:
            pass

    print("\nFinish.")


def process_regions():
    data = prepare_data(REGIONS)

    print("\n--- Seeding regions: ---")

    Polygon.objects.filter(type='region').delete()

    saved = 0

    for feature in data["features"]:
        json_region_name = feature["properties"]["name"]
        try:
            if json_region_name is None:
                continue
            region = Region.objects.get(name=json_region_name)
            polygon = Polygon(id="%s:%s" % ("region", region.id))
            polygon.type = "region"
            polygon.type_id = region.id
            polygon.polygon = json.dumps(feature["geometry"]["coordinates"])
            polygon.save()
            print(".", end="")
            saved += 1
        except (Region.DoesNotExist, Region.MultipleObjectsReturned):
            pass

    in_file = 4651

    print("""\nRegions in our database: %d,
          regions in file: %d, regions matched: %d"""
          % (len(Region.objects.all()), in_file, saved))
