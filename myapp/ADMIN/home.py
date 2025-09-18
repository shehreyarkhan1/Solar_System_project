from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from myapp.models import Inverter, HomepageSlider
import json


def homepage(request):
    sliders = HomepageSlider.objects.all().order_by("-updated_at")

    if request.method == "POST":
        
        # Handle Add Slider
        if "add" in request.POST:
            title = request.POST.get("title")
            subtitle = request.POST.get("subtitle", "")
            description = request.POST.get("description", "")
            image = request.FILES.get("image")
            cta_text = request.POST.get("cta_text", "")
            cta_link = request.POST.get("cta_link", "")
            cta_internal_page = request.POST.get("cta_internal_page", "")

            # Validation
            errors = []
            if not title:
                errors.append("Title is required")
            if not image:
                errors.append("Main image is required")

            if errors:
                for error in errors:
                    messages.error(request, error)
            else:
                try:
                    HomepageSlider.objects.create(
                        title=title,
                        subtitle=subtitle,
                        description=description,
                        image=image,
                        cta_text=cta_text,
                        cta_link=cta_link,
                        cta_internal_page=cta_internal_page,
                    )
                    messages.success(
                        request, f'Slider "{title}" has been created successfully.'
                    )
                    return redirect("homepage")
                except Exception as e:
                    messages.error(request, f"Error creating slider: {str(e)}")

        # Handle Delete Slider
        elif "delete" in request.POST:
            delete_id = request.POST.get("slider_id")
            if delete_id:
                try:
                    slider_to_delete = get_object_or_404(HomepageSlider, id=delete_id)
                    slider_title = slider_to_delete.title

                    # Delete main image only
                    if slider_to_delete.image:
                        try:
                            if slider_to_delete.image.storage.exists(slider_to_delete.image.name):
                                slider_to_delete.image.delete()
                        except Exception as e:
                            messages.warning(request, f"Image file couldn't be deleted: {str(e)}")

                    slider_to_delete.delete()
                    messages.success(
                        request, f'Slider "{slider_title}" has been deleted successfully.'
                    )

                except HomepageSlider.DoesNotExist:
                    messages.error(request, "Slider not found.")
                except Exception as e:
                    messages.error(request, f"Error deleting slider: {str(e)}")
            else:
                messages.error(request, "No slider ID provided.")
                # for update
        elif "update" in request.POST:
            slider_id=request.POST.get("slider_id")
            slider=HomepageSlider.objects.get(id=slider_id)

            title = request.POST.get("title")
            subtitle = request.POST.get("subtitle", "")
            description = request.POST.get("description", "")
            image = request.FILES.get("image")
            cta_text = request.POST.get("cta_text", "")
            cta_link = request.POST.get("cta_link", "")
            cta_internal_page = request.POST.get("cta_internal_page", "")
            if not title:
                messages.error(request, "Title is required")
                return redirect("homepage")
            
            try:
                slider.title = title
                slider.subtitle = subtitle
                slider.description = description
                slider.cta_text = cta_text
                slider.cta_link = cta_link
                slider.cta_internal_page = cta_internal_page
                if image:
                    slider.image = image

                slider.save()
                messages.success(
                    request, f'Slider "{title}" has been updated successfully.'
                )
                return redirect("homepage")
            except Exception as e:
                messages.error(request, f"Error updating slider: {str(e)}")
    return render(request, "admin/home.html", {"sliders": sliders})
