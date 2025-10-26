from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from .models import Vehicle
from .forms import PhoneLoginForm, RegistrationForm, ExtraFieldsForm

import re


class CustomLogoutView(LogoutView):
    """Foydalanuvchini tizimdan xavfsiz chiqish uchun"""
    next_page = reverse_lazy('')


class IdentifyVehicleView(LoginRequiredMixin, View):
    """Avtomobil raqamini aniqlovchi sahifa"""
    template_name = 'index.html'
    login_url = reverse_lazy('login')  # hardcoded '/' o‘rniga

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        number_plate = request.POST.get("carNumber", "").strip()
        vehicle = None

        if number_plate:
            # Normalizatsiya
            normalized = re.sub(r"\s+", "", number_plate).upper()
            normalized = re.sub(r"[^\w]", "", normalized)

            # Xavfsiz va case-insensitive qidiruv
            vehicle = Vehicle.objects.filter(vehicle_number__iexact=normalized).first()

        context = {
            "vehicle": vehicle,
            "entered_plate": number_plate,
            "DEBUG_MARKER": "IdentifyVehicleView ishlayapti!"
        }
        return render(request, self.template_name, context)


class UserLoginView(View):
    """Telefon raqam bilan tizimga kirish"""
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('search_car')  # foydalanuvchi kirdi — qayta login kerak emas
        form = PhoneLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']

            user = authenticate(request, username=username, password=password)

            if user:
                # Telefon raqam ham mosligini tekshirish
                if getattr(user, "phone_number", None) == phone_number:
                    login(request, user)
                    messages.success(request, "Muvaffaqiyatli tizimga kirdingiz!")
                    return redirect('search_car')
                else:
                    messages.error(request, "Telefon raqam noto‘g‘ri.")
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri.")
        else:
            messages.error(request, "Forma noto‘g‘ri to‘ldirilgan.")

        return render(request, self.template_name, {"form": form})


class UserRegistrationView(View):
    """Yangi foydalanuvchini ro‘yxatdan o‘tkazish"""
    template_name = 'registration.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('vehicle_registration')
        form = RegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # kerak bo‘lsa email tasdiqdan keyin False qiling
            user.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect('vehicle_registration')

        messages.error(request, "Ma'lumotlar noto‘g‘ri to‘ldirilgan.")
        return render(request, self.template_name, {'form': form})


class VehicleRegistrationView(LoginRequiredMixin, View):
    """Foydalanuvchining avtomobilini ro‘yxatdan o‘tkazish"""
    template_name = 'filling_extra_fields.html'
    login_url = reverse_lazy('login')

    def get(self, request):
        form = ExtraFieldsForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ExtraFieldsForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, "Avtomobil ro'yxatdan o'tdi.")
            return redirect('search_car')  # '/' o‘rniga nom bilan ishlatish tavsiya qilinadi
        messages.error(request, "Avtomobil ma'lumotlarini to‘ldirishda xatolik yuz berdi.")
        return render(request, self.template_name, {'form': form})
