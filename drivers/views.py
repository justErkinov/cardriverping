from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, mixins
from django.contrib import messages

from .models import Vehicle, CustomUser
from .forms import PhoneLoginForm, RegistrationForm 
import re


class IdentifyVehicleView(mixins.LoginRequiredMixin, View):
    template_name = 'index.html'
    login_url = '/'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        number_plate = request.POST.get("carNumber", "").strip()
        print("KIRITILGAN:", number_plate)
        print("KIRITILGAN repr:", repr(number_plate))  

        vehicle = None
        if number_plate:
            normalized = re.sub(r"\s+", "", number_plate).upper()
            normalized = re.sub(r"[^\w]", "", normalized)  
            print("NORMALIZED:", normalized)
            print("NORMALIZED repr:", repr(normalized))  

            vehicle = Vehicle.objects.filter(vehicle_number__iexact=normalized).first()
            print("TOPILDI:", vehicle)

        return render(request, self.template_name, {
            "vehicle": vehicle,
            "entered_plate": number_plate,
            "DEBUG_MARKER": "IdentifyVehicleView ishlayapti!" 
        })


class UserLoginView(View):
    template_name = 'login.html' 

    def get(self, request):
        form = PhoneLoginForm()  
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PhoneLoginForm(request.POST)  
        if form.is_valid():
            username = form.cleaned_data['username']  
            password = form.cleaned_data['password'] 
            phone_number = form.cleaned_data['phone_number']  
        
            user = authenticate(request, username=username, password=password)
            
            if user and getattr(user, "phone_number", None) == phone_number:
                login(request, user)  
                messages.success(request, "Muvaffaqiyatli tizimga kirdingiz!")
                return redirect('/search/')  
            messages.error(request, "Foydalanuvchi nomi, parol yoki telefon raqam noto'g'ri.")

        return render(request, "login.html", {"form": form})
    

class UserRegistrationView(View):
    template_name = 'registration.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect('/')
        return render(request, self.template_name, {'form': form})