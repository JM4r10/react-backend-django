from customers.models import Customer
from django.http import JsonResponse, Http404
from customers.serializer import CustomerSerializer
from rest_framework.decorators import api_view, permission_classes  # says which methods are allowed
# use it for all responses: JSON response, 404, etc
from rest_framework.response import Response
from rest_framework import status  # options for status codes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def customers(request):
    # invokes serializer and return to client
    if request.method == 'GET':
        data_db = Customer.objects.all()
        serializer = CustomerSerializer(data_db, many=True)
        return Response({'customers':serializer.data})
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'customer':serializer.data}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def customer(request, id):
    try:
        data_db = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # raise Exception()
        serializer = CustomerSerializer(data_db)
        return Response({'customer': serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        data_db.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    elif request.method == 'POST':
        serializer = CustomerSerializer(data_db, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'customer':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)