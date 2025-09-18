from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from myapp.models import Inverter
import json


class Products(View):
    def get(self, request):
        inverters = Inverter.objects.all()
        return render(request, "admin/products.html", {"inverters": inverters})

    def post(self, request):
        if request.POST.get("delete_id"):
            return self.delete_inverter(request)

        inverter_id = request.POST.get("id")
        if inverter_id:
            return self.update_inverter(request, inverter_id)

        return self.create_inverter(request)

    def validate_input(self, data, files):
        errors = []

        required_fields = [
            "name",
            "brand",
            "model",
            "power_capacity_kw",
            "input_voltage",
            "output_voltage",
            "price",
            "description",
        ]

        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field.replace('_', ' ').title()} is required.")

        # Check numeric fields
        for num_field in ["price", "power_capacity_kw"]:
            try:
                float(data.get(num_field))
            except (ValueError, TypeError):
                errors.append(
                    f"{num_field.replace('_', ' ').title()} must be a number."
                )

        # Validate image (optional)
        image = files.get("image")
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB max
                errors.append("Image size must be less than 5MB.")

        return errors

    def create_inverter(self, request):
        errors = self.validate_input(request.POST, request.FILES)

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(
                request, "admin/products.html", {"inverters": Inverter.objects.all()}
            )

        try:
            Inverter.objects.create(
                name=request.POST.get("name"),
                brand=request.POST.get("brand"),
                model=request.POST.get("model"),
                power_capacity_kw=request.POST.get("power_capacity_kw"),
                input_voltage=request.POST.get("input_voltage"),
                output_voltage=request.POST.get("output_voltage"),
                price=request.POST.get("price"),
                image=request.FILES.get("image"),
                description=request.POST.get("description"),
            )
            messages.success(request, "Inverter created successfully!")
            return redirect("products")

        except Exception as e:
            messages.error(request, f"Error creating inverter: {str(e)}")
            return render(
                request, "admin/products.html", {"inverters": Inverter.objects.all()}
            )

    def update_inverter(self, request, inverter_id):
        inverter = get_object_or_404(Inverter, id=inverter_id)

        errors = self.validate_input(request.POST, request.FILES)

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect("products")

        try:
            inverter.name = request.POST.get("name", inverter.name)
            inverter.brand = request.POST.get("brand", inverter.brand)
            inverter.model = request.POST.get("model", inverter.model)
            inverter.power_capacity_kw = request.POST.get(
                "power_capacity_kw", inverter.power_capacity_kw
            )
            inverter.input_voltage = request.POST.get(
                "input_voltage", inverter.input_voltage
            )
            inverter.output_voltage = request.POST.get(
                "output_voltage", inverter.output_voltage
            )
            inverter.price = request.POST.get("price", inverter.price)
            inverter.description = request.POST.get("description", inverter.description)

            if request.FILES.get("image"):
                inverter.image = request.FILES.get("image")

            inverter.save()
            messages.success(request, "Inverter updated successfully!")
            return redirect("products")

        except Exception as e:
            messages.error(request, f"Error updating inverter: {str(e)}")
            return redirect("products")

    def delete_inverter(self, request):
        inverter_id = request.POST.get("delete_id")
        try:
            inverter = Inverter.objects.get(id=inverter_id)
            inverter.delete()
            messages.success(request, "Inverter deleted successfully!")
        except Inverter.DoesNotExist:
            messages.error(request, "Inverter not found.")
        except Exception as e:
            messages.error(request, f"Error deleting inverter: {str(e)}")
        return redirect("products")
