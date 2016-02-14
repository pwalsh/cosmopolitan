[![Build Status](https://travis-ci.org/openspending/cosmopolitan.svg?branch=master)](https://travis-ci.org/openspending/cosmopolitan) [![Coverage Status](https://coveralls.io/repos/openspending/cosmopolitan/badge.svg?branch=master&service=github)](https://coveralls.io/github/openspending/cosmopolitan?branch=master)

# Cosmopolitan
An API server for core data on places of the world.

http://cosmopolitan.openspending.org/

This API provides information about countries, cities and currencies all over the world and can be used as a cataloged data for various reasons.

Just a brief summary:

* contains a list of all countries in the world with country code, country continent and list of countries on the same continent;
* contains a list of all continents in the world with a list of countries for each continent;
* contains a list of all currencies in the world, each currency has a list of countries where this currency is being used.

Based on https://github.com/coderholic/django-cities

## Using the API

Add param `format=json` in every request you want to perform to get JSON responses.
For example: `GET /v1/?format=json`.

API has self-documented format, so when you request to `/` (root of the API without any params) you'll get descriptions of all endpoints and can follow them for more descriptions.

You could also use filters when using this API:

### Filter countries by continents

* `/v1/countries/?continents={id}` - get countries of the particular continent;
* `/v1/countries/?continents={id},{id},{id}` - get countries belongs to several continents.

Example: `GET /v1/countries/?continents=an`, `GET /v1/countries/?continents=an,af`

### Filter currencies by countries

* `/v1/currencies/?countries={id}` - get currencies of the particular country;
* `/v1/currencies/?countries={id},{id},{id}` - get currencies belongs to several countries.

Example: `GET /v1/currencies/?countries=aq`, `GET /v1/currencies/?countries=aq,af`


## Running locally

Under virtual env (to create virtualenv, run `python3 -m venv env`):

    source env/bin/activate

    export LOCAL_DEV=1

    export DEBUG=1

Postgres + PostGIS setup (OS X):

    brew install postgis

    createuser cosmopolitan

    createdb cosmopolitan

    psql cosmopolitan

    alter user "cosmopolitan" with password '123456';

    grant all privileges on database cosmopolitan to cosmopolitan;

    CREATE EXTENSION postgis;

## Starting from scratch

### Requirements

* [GDAL/OGR Binaries](http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries)

if you just pulled this repo, you need to:

* migrate database: `./manage.py migrate`

* fill in cities database with `./manage.py cities --import=all`;

## License

`Cosmopolitan` is opensource, licensed under a standard MIT license (included in this repository as [LICENSE](https://github.com/openspending/cosmopolitan/blob/master/LICENSE)).

Data sources licensies:

- [GeoNames](http://www.geonames.org/about.html) is under a creative commons attribution license.
- [NaturalEarthData terms of use](naturalearthdata.com/about/terms-of-use/)
