from django.urls import path
from . import views
urlpatterns = [
    path("", views.buildurl, name="buildurl"),
    path("lookuptable/", views.lookuptable, name="lookuptable"),
]