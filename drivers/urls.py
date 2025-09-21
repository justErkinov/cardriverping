from django.urls import path
from .views import IdentifyVehicleView, UserLoginView, UserRegistrationView, CustomLogoutView

urlpatterns = [
    path("search/", IdentifyVehicleView.as_view(), name="search_car"),
    path("", UserLoginView.as_view(), name="login"),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    path("register/", UserRegistrationView.as_view(), name='registration')
]

