from django.views import View
from django.shortcuts import render
from myapp.models import Inverter


class Dashboard(View):

    def get(self, request):
        inverters = Inverter.objects.all()
        inverter_count = inverters.count()
        return render(request,"admin/dashboard.html",{"inverter": inverters, "inverter_count": inverter_count},
        )
