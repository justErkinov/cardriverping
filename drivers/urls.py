from django.urls import path
from .views import IdentifyVehicleView, PhoneLoginView

urlpatterns = [
    path("search/", IdentifyVehicleView.as_view(), name="search_car"),
    path("login/", PhoneLoginView.as_view(), name="phone_login"),
]