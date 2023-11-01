from django.urls import path
from . import views
urlpatterns = [
    path("", views.buildurl, name="buildurl"),
    path("lookuptable/<build_url>", views.lookuptable, name="lookuptable"),
]