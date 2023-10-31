from django.urls import path
from . import views
urlpatterns = [
    path("", views.login, name="login"),
    path("buildurl/", views.buildurl, name="buildurl"),
    path("lookuptable/", views.lookuptable, name="lookuptable"),
]