from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):# To print the object as a string
        return f"{self.city} - ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def isValidFlight(self):
        return (self.origin != self.destination) and (self.duration > 0)

    def __str__(self):# To print the object as a string
        return f"{self.id} - {self.origin} to {self.destination}"

class Passenger(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.firstName} {self.lastName}"