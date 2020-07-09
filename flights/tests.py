from django.db.models import Max
from django.test import TestCase, Client

from .models import Airport, Flight, Passenger

# Create your tests here.
class ModelsTestCase(TestCase):
    def setUp(self):
        #Create airports
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        #Create flights
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)
    
    def testDeparturesCount(self):
        a = Airport.objects.get(code = "AAA")
        self.assertEqual(a.departures.count(), 3)
    
    def testArrivalsCount(self):
        a = Airport.objects.get(code = "AAA")
        self.assertEqual(a.arrivals.count(), 1)
    
    def testValidFlight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.isValidFlight())

    def testInvalidFlightDestination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.isValidFlight())

    def testInvalidFlightDuration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.isValidFlight())
    
    def testIndex(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)
    
    def testValidFlightPage(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
    
    def testInvalidFlightPage(self):
        maxId = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/{maxId + 1}")
        self.assertEqual(response.status_code, 404)
    
    def testFlightPagePassengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(firstName="Alice", lastName="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)
    
    def testFlightPageNonpassengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(firstName="Alice", lastName="Adams")

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)