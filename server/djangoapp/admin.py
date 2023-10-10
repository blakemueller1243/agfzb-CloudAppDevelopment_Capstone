from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.TabularInline):  # or admin.StackedInline for a different display style
    model = CarModel
    extra = 1  # Number of empty forms to display for adding CarModel instances when editing a CarMake

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
