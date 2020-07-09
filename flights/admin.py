from django.contrib import admin
from .models import Airport, Flight, Passenger

# Register your models here.
class PassengerInline(admin.StackedInline):# StackedInline is a class from django.admin that lets you add relationship between objects
    model = Passenger.flights.through #This references the many-to-many table between Flight and Passenger
    extra = 1

class FlightAdmin(admin.ModelAdmin):
    inlines = [PassengerInline]

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)