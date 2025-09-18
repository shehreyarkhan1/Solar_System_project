from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from django.http import JsonResponse
from myapp.models import Inverter,HomepageSlider
import json


def index(request):
    sliders=HomepageSlider.objects.all().order_by("-created_at")

    return render(request, "index.html",{"sliders":sliders})


