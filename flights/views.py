from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    context = {
        "flights": Flight.objects.all()
    }
    # return HttpResponse("Hello-world")
    return render(request, 'flights/index.html', context)

def flight(request, flight_id):#flight_id is a second argument because it was provided as a parameter in the url
    try:
        flight = Flight.objects.get(pk = flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight Does not exist.")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights= flight).all()
    }
    return render(request, 'flights/flight.html', context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk = passenger_id)
        flight = Flight.objects.get(pk = flight_id)
        print(passenger)
        print(flight)
    except KeyError:# If the user didn't pass-in data with the request
        return render(request, "flights/error.html", {"message": "No selection"})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No Flight."})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No Passenger."})
    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
