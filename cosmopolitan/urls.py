from django.conf.urls import include
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers

from world.views import ContinentViewSet
from world.views import CurrencyViewSet
from world.views import CountryViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'countries', CountryViewSet)
router.register(r'continents', ContinentViewSet)
router.register(r'currencies', CurrencyViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^v1/', include(router.urls)),
]
urlpatterns += staticfiles_urlpatterns()
