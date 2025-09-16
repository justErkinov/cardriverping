from django.urls import path
from .views import IdentifyVehicleView

urlpatterns = [
    path("search/", IdentifyVehicleView.as_view(), name="search_car"),
]