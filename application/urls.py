from django.conf.urls import include
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers

from cosmopolitan.viewsets import ContinentViewSet
from cosmopolitan.viewsets import CountryViewSet
from cosmopolitan.viewsets import RegionViewSet
from cosmopolitan.viewsets import CityViewSet
from cosmopolitan.viewsets import CurrencyViewSet
from cosmopolitan.viewsets import PostcodeViewSet
from cosmopolitan.viewsets import PolygonViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'continents', ContinentViewSet)
router.register(r'countries', CountryViewSet, base_name='country')
router.register(r'regions', RegionViewSet, base_name='region')
router.register(r'cities', CityViewSet, base_name='city')
router.register(r'currencies', CurrencyViewSet, base_name='currency')
router.register(r'postcodes', PostcodeViewSet, base_name='postcode')
router.register(r'polygons', PolygonViewSet, base_name='polygon')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^v1/', include(router.urls)),
]
urlpatterns += staticfiles_urlpatterns()
