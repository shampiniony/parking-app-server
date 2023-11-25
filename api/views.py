from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Parking, Parkomat, Terminal, Comment
from .serializer import ParkingSerializer, TerminalSerializer, ParkomatSerializer, CommentSerializer
from rest_framework import status
from .utils import load_parkings_from_ek, create_payment, get_payment_link, get_payment_status
import datetime


# Create your views here.

@api_view(['POST'])
def parking_reserve(request, parking_id):
    parking = get_object_or_404(Parking, id=parking_id)
    credentials = request.data.get('credentials')
    if credentials is None:
        return Response({"error": "no credentials"})
    # надо случайный
    return Response({
        "payment_id": "todo",
        "payment_link": get_payment_link("todo")
    })


@api_view(['GET'])
def payment_status(request):
    payment_id = request.data.get('payment_id')
    if payment_id is None:
        return Response({"error": "no payment_id"})
    pay_status = get_payment_status(payment_id)
    return Response({
        "status": pay_status
    })


@api_view(['GET'])
def get_parkings(request):
    parkings = Parking.objects.all()
    serializer = ParkingSerializer(parkings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_terminals(request):
    terminals = Terminal.objects.all()
    serializer = TerminalSerializer(terminals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_parkomats(request):
    parkomats = Parkomat.objects.all()
    serializer = ParkomatSerializer(parkomats, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def put_comment(request, parking_id):
    parking = get_object_or_404(Parking, id=parking_id)
    text = request.data.get('text')
    if text is None:
        return Response({"error": "no text"})
    comment = Comment(
        parking=parking,
        text=text
    )
    comment.save()
    return Response({"success": "Data uploaded successfully"})


@api_view(['GET'])
def get_comments(request, parking_id):
    parking = get_object_or_404(Parking, id=parking_id)
    comments = parking.comment_set.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_parking_by_id(request, parking_id):
    # Get the parking object based on the provided ID or return a 404 response
    parking = get_object_or_404(Parking, id=parking_id)

    # Serialize the parking object
    serializer = ParkingSerializer(parking)

    # Return the serialized data as JSON
    return Response(serializer.data)


@api_view(['PUT'])
def put_ek(request):
    json_data = request.data['parkings']
    if not json_data:
        return Response({'error': 'JSON data is required'}, status=status.HTTP_400_BAD_REQUEST)

    load_parkings_from_ek(json_data)
    return Response({'success': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
