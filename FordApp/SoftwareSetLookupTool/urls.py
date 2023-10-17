from django.urls import path
from . import views
urlpatterns = [
    path("", views.login, name="login"),
    path("projects/", views.buildurl, name="buildurl"),
    path("contact/", views.lookuptable, name="lookuptable"),
]