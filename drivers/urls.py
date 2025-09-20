from django.urls import path
from .views import IdentifyVehicleView, UserLoginView, UserRegistrationView

urlpatterns = [
    path("search/", IdentifyVehicleView.as_view(), name="search_car"),
    path("", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name='registration')
]