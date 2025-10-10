from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from django.http import JsonResponse
from myapp.models import Inverter,HomepageSlider
import json


def index(request):
    sliders = HomepageSlider.objects.all().order_by("-created_at")
    inverter = Inverter.objects.all().order_by("-created_at")
    
    # Create JSON data for JavaScript
    products_data = []
    for inv in inverter:
        # Determine icon based on product name
        if 'Residential' in inv.name:
            icon = "🏠"
        elif 'Commercial' in inv.name:
            icon = "🏢"
        elif 'Industrial' in inv.name:
            icon = "🏭"
        else:
            icon = "⚡"
        
        product = {
            'name': inv.name,
            'brand': inv.brand,
            'model': inv.model,
            'power': float(inv.power_capacity_kw),
            'input': inv.input_voltage,
            'output': inv.output_voltage,
            'price': float(inv.price),
            'description': inv.description or '',
            'image': inv.image.url if inv.image else '',
            'icon': icon
        }
        products_data.append(product)
    
    products_json = json.dumps(products_data)
    
    return render(request, "index.html", {
        "sliders": sliders,
        "inverter": inverter,
        "products_json": products_json
    })

    


