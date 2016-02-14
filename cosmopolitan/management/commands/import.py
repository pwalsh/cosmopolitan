from __future__ import print_function

from optparse import make_option

from django.core.management.base import BaseCommand
import cosmopolitan.management.commands._django_cities as ds
import cosmopolitan.management.commands._naturalearthdata as ned

# more stuff could be added here
IMPORT_OPTS = [
    "all",
    "django_cities",
    "naturalearthdata"
]


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
        ds.process_continents()
        ds.process_countries()
        ds.process_currencies()
        ds.process_relations()

        ds.process_regions()
        ds.process_cities()

        ds.process_postcodes()
        ds.add_regions_to_postcodes()

    def _import_naturalearthdata(self):
        ned.process_countries()

    def _import_all(self):
        self._import_django_cities()
        self._import_naturalearthdata()
        print("\nImport finished")
