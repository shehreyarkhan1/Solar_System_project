from django.db import models
import os
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Will store hashed password
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


# Create your models here.
class Inverter(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    power_capacity_kw = models.FloatField()
    input_voltage = models.CharField(max_length=50)
    output_voltage = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="inverters/", null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # TEMPORARY
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = Inverter.objects.get(pk=self.pk)
                if old_instance.image and old_instance.image != self.image:
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
            except Inverter.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.name}"


class HomepageSlider(models.Model):
    title = models.CharField(max_length=200, help_text="Main headline")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Secondary text")
    description = models.TextField(blank=True, help_text="Brief description")
    image = models.ImageField(upload_to="slider/", help_text="Recommended: 1920x800px")
    # Call-to-action
    cta_text = models.CharField(max_length=50, blank=True, help_text="Button text")
    cta_link = models.URLField(blank=True, help_text="Button link")
    cta_internal_page = models.CharField(
        max_length=100,
        blank=True,
        help_text="Internal page name (e.g., 'products', 'contact')",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
