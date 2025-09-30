from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import DatabaseError, OperationalError, IntegrityError
from myapp.models import Inverter, HomepageSlider
import json
import logging

# Configure logger
logger = logging.getLogger(__name__)


def homepage(request):
    """
    Handle homepage slider management with proper error handling.
    """
    try:
        # Fetch all sliders with error handling
        try:
            sliders = HomepageSlider.objects.all().order_by("-updated_at")
        except DatabaseError as e:
            logger.error(f"Database error fetching sliders: {str(e)}")
            messages.error(
                request, "Unable to load sliders. Database connection error."
            )
            sliders = []
        except Exception as e:
            logger.error(f"Error fetching sliders: {str(e)}")
            messages.error(request, "Unable to load sliders. Please try again.")
            sliders = []

        if request.method == "POST":
            try:
                # Handle Add Slider
                if "add" in request.POST:
                    try:
                        # Get form data with safe defaults
                        title = request.POST.get("title", "").strip()
                        subtitle = request.POST.get("subtitle", "").strip()
                        description = request.POST.get("description", "").strip()
                        image = request.FILES.get("image")
                        cta_text = request.POST.get("cta_text", "").strip()
                        cta_link = request.POST.get("cta_link", "").strip()
                        cta_internal_page = request.POST.get(
                            "cta_internal_page", ""
                        ).strip()

                        # Validation
                        errors = []

                        if not title:
                            errors.append("Title is required")
                        elif len(title) > 200:
                            errors.append("Title must be less than 200 characters")

                        if not image:
                            errors.append("Main image is required")
                        else:
                            # Validate image file
                            try:
                                # Check file size (e.g., max 5MB)
                                if image.size > 5 * 1024 * 1024:
                                    errors.append(
                                        "Image file size must be less than 5MB"
                                    )

                                # Check file type
                                allowed_types = [
                                    "image/jpeg",
                                    "image/jpg",
                                    "image/png",
                                    "image/webp",
                                    "image/gif",
                                ]
                                if (
                                    hasattr(image, "content_type")
                                    and image.content_type not in allowed_types
                                ):
                                    errors.append(
                                        "Image must be JPEG, PNG, WEBP, or GIF format"
                                    )
                            except Exception as e:
                                logger.error(f"Image validation error: {str(e)}")
                                errors.append("Unable to validate image file")

                        if subtitle and len(subtitle) > 300:
                            errors.append("Subtitle must be less than 300 characters")

                        if description and len(description) > 1000:
                            errors.append(
                                "Description must be less than 1000 characters"
                            )

                        if cta_text and len(cta_text) > 100:
                            errors.append("CTA text must be less than 100 characters")

                        if cta_link and len(cta_link) > 500:
                            errors.append("CTA link must be less than 500 characters")

                        if errors:
                            for error in errors:
                                messages.error(request, error)
                            return render(
                                request, "admin/home.html", {"sliders": sliders}
                            )

                        try:
                            # Create slider
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
                                request,
                                f'Slider "{title}" has been created successfully.',
                            )
                            logger.info(f"Slider created: {title}")
                            return redirect("homepage")

                        except IntegrityError as e:
                            logger.error(
                                f"Database integrity error creating slider: {str(e)}"
                            )
                            messages.error(
                                request, "Slider with this information already exists."
                            )

                        except DatabaseError as e:
                            logger.error(f"Database error creating slider: {str(e)}")
                            messages.error(
                                request, "Database error. Unable to create slider."
                            )

                        except ValidationError as e:
                            logger.error(f"Validation error creating slider: {str(e)}")
                            messages.error(request, f"Validation error: {str(e)}")

                        except Exception as e:
                            logger.error(f"Unexpected error creating slider: {str(e)}")
                            messages.error(request, f"Error creating slider: {str(e)}")

                    except Exception as e:
                        logger.error(f"Error processing add slider request: {str(e)}")
                        messages.error(
                            request, "Error processing your request. Please try again."
                        )

                # Handle Delete Slider
                elif "delete" in request.POST:
                    try:
                        delete_id = request.POST.get("slider_id", "").strip()

                        if not delete_id:
                            messages.error(request, "No slider ID provided.")
                            return render(
                                request, "admin/home.html", {"sliders": sliders}
                            )

                        # Validate ID is numeric
                        try:
                            delete_id = int(delete_id)
                        except (ValueError, TypeError):
                            messages.error(request, "Invalid slider ID.")
                            return render(
                                request, "admin/home.html", {"sliders": sliders}
                            )

                        try:
                            slider_to_delete = get_object_or_404(
                                HomepageSlider, id=delete_id
                            )
                            slider_title = slider_to_delete.title

                            # Delete main image
                            if slider_to_delete.image:
                                try:
                                    if hasattr(slider_to_delete.image, "storage"):
                                        if slider_to_delete.image.storage.exists(
                                            slider_to_delete.image.name
                                        ):
                                            slider_to_delete.image.delete(save=False)
                                except Exception as e:
                                    logger.warning(
                                        f"Image file couldn't be deleted: {str(e)}"
                                    )
                                    # Continue with slider deletion even if image deletion fails

                            # Delete slider
                            slider_to_delete.delete()
                            messages.success(
                                request,
                                f'Slider "{slider_title}" has been deleted successfully.',
                            )
                            logger.info(f"Slider deleted: {slider_title}")
                            return redirect("homepage")

                        except HomepageSlider.DoesNotExist:
                            logger.warning(
                                f"Attempt to delete non-existent slider ID: {delete_id}"
                            )
                            messages.error(request, "Slider not found.")

                        except DatabaseError as e:
                            logger.error(f"Database error deleting slider: {str(e)}")
                            messages.error(
                                request, "Database error. Unable to delete slider."
                            )

                        except Exception as e:
                            logger.error(f"Error deleting slider: {str(e)}")
                            messages.error(request, f"Error deleting slider: {str(e)}")

                    except Exception as e:
                        logger.error(
                            f"Error processing delete slider request: {str(e)}"
                        )
                        messages.error(
                            request,
                            "Error processing delete request. Please try again.",
                        )

                # Handle Update Slider
                elif "update" in request.POST:
                    try:
                        slider_id = request.POST.get("slider_id", "").strip()

                        if not slider_id:
                            messages.error(request, "No slider ID provided.")
                            return redirect("homepage")

                        # Validate ID is numeric
                        try:
                            slider_id = int(slider_id)
                        except (ValueError, TypeError):
                            messages.error(request, "Invalid slider ID.")
                            return redirect("homepage")

                        try:
                            slider = get_object_or_404(HomepageSlider, id=slider_id)
                        except HomepageSlider.DoesNotExist:
                            logger.warning(
                                f"Attempt to update non-existent slider ID: {slider_id}"
                            )
                            messages.error(request, "Slider not found.")
                            return redirect("homepage")

                        try:
                            # Get form data
                            title = request.POST.get("title", "").strip()
                            subtitle = request.POST.get("subtitle", "").strip()
                            description = request.POST.get("description", "").strip()
                            image = request.FILES.get("image")
                            cta_text = request.POST.get("cta_text", "").strip()
                            cta_link = request.POST.get("cta_link", "").strip()
                            cta_internal_page = request.POST.get(
                                "cta_internal_page", ""
                            ).strip()

                            # Validation
                            errors = []

                            if not title:
                                errors.append("Title is required")
                            elif len(title) > 200:
                                errors.append("Title must be less than 200 characters")

                            if subtitle and len(subtitle) > 300:
                                errors.append(
                                    "Subtitle must be less than 300 characters"
                                )

                            if description and len(description) > 1000:
                                errors.append(
                                    "Description must be less than 1000 characters"
                                )

                            if cta_text and len(cta_text) > 100:
                                errors.append(
                                    "CTA text must be less than 100 characters"
                                )

                            if cta_link and len(cta_link) > 500:
                                errors.append(
                                    "CTA link must be less than 500 characters"
                                )

                            # Validate image if provided
                            if image:
                                try:
                                    if image.size > 5 * 1024 * 1024:
                                        errors.append(
                                            "Image file size must be less than 5MB"
                                        )

                                    allowed_types = [
                                        "image/jpeg",
                                        "image/jpg",
                                        "image/png",
                                        "image/webp",
                                        "image/gif",
                                    ]
                                    if (
                                        hasattr(image, "content_type")
                                        and image.content_type not in allowed_types
                                    ):
                                        errors.append(
                                            "Image must be JPEG, PNG, WEBP, or GIF format"
                                        )
                                except Exception as e:
                                    logger.error(f"Image validation error: {str(e)}")
                                    errors.append("Unable to validate image file")

                            if errors:
                                for error in errors:
                                    messages.error(request, error)
                                return redirect("homepage")

                            try:
                                # Update slider fields
                                slider.title = title
                                slider.subtitle = subtitle
                                slider.description = description
                                slider.cta_text = cta_text
                                slider.cta_link = cta_link
                                slider.cta_internal_page = cta_internal_page

                                # Update image if provided
                                if image:
                                    # Delete old image before replacing
                                    if slider.image:
                                        try:
                                            if hasattr(slider.image, "storage"):
                                                if slider.image.storage.exists(
                                                    slider.image.name
                                                ):
                                                    slider.image.delete(save=False)
                                        except Exception as e:
                                            logger.warning(
                                                f"Old image couldn't be deleted: {str(e)}"
                                            )

                                    slider.image = image

                                slider.save()
                                messages.success(
                                    request,
                                    f'Slider "{title}" has been updated successfully.',
                                )
                                logger.info(f"Slider updated: {title}")
                                return redirect("homepage")

                            except IntegrityError as e:
                                logger.error(
                                    f"Database integrity error updating slider: {str(e)}"
                                )
                                messages.error(
                                    request,
                                    "Database integrity error. Unable to update slider.",
                                )

                            except DatabaseError as e:
                                logger.error(
                                    f"Database error updating slider: {str(e)}"
                                )
                                messages.error(
                                    request, "Database error. Unable to update slider."
                                )

                            except ValidationError as e:
                                logger.error(
                                    f"Validation error updating slider: {str(e)}"
                                )
                                messages.error(request, f"Validation error: {str(e)}")

                            except Exception as e:
                                logger.error(f"Error updating slider: {str(e)}")
                                messages.error(
                                    request, f"Error updating slider: {str(e)}"
                                )

                        except Exception as e:
                            logger.error(f"Error processing slider update: {str(e)}")
                            messages.error(
                                request, "Error processing update. Please try again."
                            )

                    except Exception as e:
                        logger.error(f"Error in update slider handler: {str(e)}")
                        messages.error(
                            request,
                            "Error processing update request. Please try again.",
                        )

                else:
                    logger.warning("Unknown POST action in homepage view")
                    messages.warning(request, "Unknown action requested.")

            except Exception as e:
                logger.error(f"Error processing POST request in homepage: {str(e)}")
                messages.error(
                    request, "Error processing your request. Please try again."
                )

        # Render the page
        return render(request, "admin/home.html", {"sliders": sliders})

    except Exception as e:
        # Top-level catch-all for any unexpected errors
        logger.critical(f"Critical error in homepage view: {str(e)}")
        try:
            messages.error(
                request, "A critical error occurred. Please contact support."
            )
            return render(request, "admin/home.html", {"sliders": []})
        except:
            # If rendering fails, return JSON error
            return JsonResponse(
                {"error": "A critical error occurred. Please try again later."},
                status=500,
            )
