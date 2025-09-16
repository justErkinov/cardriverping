from django.shortcuts import render
from django.views import View

from .models import Vehicle

import re
# Create your views here.



class IdentifyVehicleView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        number_plate = request.POST.get("carNumber", "").strip()
        print("KIRITILGAN:", number_plate)
        print("KIRITILGAN repr:", repr(number_plate))  # 👈 ko‘rinmas belgilarni tekshirish

        vehicle = None
        if number_plate:
            normalized = re.sub(r"\s+", "", number_plate).upper()
            normalized = re.sub(r"[^\w]", "", normalized)  # 👈 faqat harf/raqam qoldiramiz
            print("NORMALIZED:", normalized)
            print("NORMALIZED repr:", repr(normalized))  # 👈 yana tekshiruv

            vehicle = Vehicle.objects.filter(vehicle_number__iexact=normalized).first()
            print("TOPILDI:", vehicle)

        return render(request, self.template_name, {
            "vehicle": vehicle,
            "entered_plate": number_plate,
            "DEBUG_MARKER": "IdentifyVehicleView ishlayapti!" 
        })
