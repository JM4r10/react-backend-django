from customers.models import Customer
from django.http import JsonResponse
from customers.serializer import CustomerSerializer

def customers(request):
    #invoke serializer and return to client
    data = Customer.objects.all()
    serializer = CustomerSerializer(data, many=True)
    return JsonResponse({'customers': serializer.data})