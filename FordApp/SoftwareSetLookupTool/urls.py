from django.urls import path
from . import views
urlpatterns = [
    path("", views.buildurl, name="buildurl"),
    path("buildurl/", views.lookuptable, name="lookuptable"),
]