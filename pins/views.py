from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from boards.models import Board
from pins.models import Pin, Pin_Board, PinImage
from pins.serializers import PinSerializer


# Create your views here.
class CreatePin(GenericAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            board = Board.objects.get(id=data['board_id'])
        except Board.DoesNotExist:
            return Response({"Error": "Board not found"}, status=404)

        if board.owner != request.user and not request.is_superuser:
            return Response({"Error": "You are not the owner of this board"}, status=403)

        pin = Pin.objects.create(title=data['title'], board=board, description=data['description'])
        try:
            pin_board = Pin_Board.objects.create(pin=pin, board=board)
            images = request.FILES.getlist('images')
            for image in images:
                PinImage.objects.create(pin=pin, image=image)
        except Exception as e:
            pin.delete()
            return Response({"Error": str(e)}, status=400)
        return Response({"Message": "Pin created successfully"}, status=201)
