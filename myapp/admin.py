from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Inverter


@admin.register(Inverter)
class InverterAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'model', 'power_capacity_kw', 'price', 'image_preview', 'actions_column']
    list_filter = ['brand', 'power_capacity_kw']
    search_fields = ['name', 'brand', 'model']
    list_per_page = 20
    ordering = ['-id']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'brand', 'model')
        }),
        ('Technical Specifications', {
            'fields': ('power_capacity_kw', 'input_voltage', 'output_voltage'),
            'classes': ('collapse',)
        }),
        ('Commercial Information', {
            'fields': ('price', 'image', 'description')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"
    
    def actions_column(self, obj):
        return format_html(
            '<a class="button" href="{}">View</a>&nbsp;'
            '<a class="button" href="{}">Edit</a>',
            reverse('admin:myapp_inverter_change', args=[obj.pk]),
            reverse('admin:myapp_inverter_change', args=[obj.pk])
        )
    actions_column.short_description = "Actions"
    actions_column.allow_tags = True


# Custom admin site configuration
admin.site.site_header = "Inverter Management System"
admin.site.site_title = "Inverter Admin"
admin.site.index_title = "Welcome to Inverter Dashboard"