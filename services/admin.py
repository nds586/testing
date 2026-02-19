from django.contrib import admin

from services.models import ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'basePrice')
    search_fields = ('name',)
