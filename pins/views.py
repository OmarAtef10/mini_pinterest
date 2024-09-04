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


class ViewPin():
    def get_pin(self, pk):
        try:
            pin = Pin.objects.get(id=pk)
            try:
                pin_images = PinImage.objects.filter(pin=pin)
            except PinImage.DoesNotExist:
                pin_images = []

            return {
                "id": pin.id,
                "title": pin.title,
                "board": pin.board.name,
                "description": pin.description,
                "images": [image.image.url for image in pin_images],
                "created_at": pin.created_at,
                "updated_at": pin.updated_at
            }
        except Pin.DoesNotExist:
            return None


class GetAllPins(GenericAPIView, ViewPin):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pins = Pin.objects.all()
        data = []
        for pin in pins:
            data.append(self.get_pin(pin.id))
        return Response(data, status=200)


class GetPinsByBoard(GenericAPIView, ViewPin):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return Response({"Error": "Board not found"}, status=404)

        if board.is_private and not request.user.is_superuser:
            if board.owner != request.user:
                return Response({"Error": "Sorry can't view a private board."}, status=403)

        pins = Pin.objects.filter(board=board)
        data = []
        for pin in pins:
            data.append(self.get_pin(pin.id))
        return Response(data, status=200)


class GetPinById(GenericAPIView, ViewPin):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            pin = Pin.objects.get(id=pk)
        except:
            return Response({"Error": "Pin not found"}, status=404)

        if pin.board.is_private and not request.user.is_superuser:
            if pin.board.owner != request.user:
                return Response({"Error": "Bummer this pin belongs to a private board"}, status=403)

        data = self.get_pin(pk)
        if data:
            return Response(data, status=200)
        return Response({"Error": "Pin not found"}, status=404)
