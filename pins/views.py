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


class UpdatePin(GenericAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            pin = Pin.objects.get(id=pk)
        except Pin.DoesNotExist:
            return Response({"Error": "Pin not found!"}, status=404)

        if pin.board.is_private and not request.user.is_superuser:
            if pin.board.owner != request.user:
                return Response({"Error": "Bummer you dont have access to this pin"})

        pin.delete()
        return Response({"Message": "Pin deleted successfully"}, status=200)

    def put(self, request, pk):
        try:
            pin = Pin.objects.get(id=pk)
        except Pin.DoesNotExist:
            return Response({"Error": "Pin not found!"}, status=404)

        if pin.board.is_private and not request.user.is_superuser:
            if pin.board.owner != request.user:
                return Response({"Error": "Bummer you dont have access to this pin"})

        data = request.data
        board_id = data.get('board_id', None)
        title = data.get('title', None)
        description = data.get('description', None)

        if board_id:
            try:
                board = Board.objects.get(id=data['board_id'])
            except Board.DoesNotExist:
                return Response({"Error": "Board not found"}, status=404)

            if board.owner != request.user and not request.is_superuser:
                return Response({"Error": "You are not the owner of this board"}, status=403)
            pin.board = board

        if title:
            pin.title = title

        if description:
            pin.description = description

        pin.save()
        serializer = PinSerializer(pin)

        return Response({"Message": "Pin updated successfully", "Pin": serializer.data}, status=200)


class UpdatePinImage(GenericAPIView):
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticated]
    queryset = Pin.objects.all()

    def delete(self, request, pin_id, image_id):
        try:
            pin = Pin.objects.get(id=pin_id)
        except Pin.DoesNotExist:
            return Response({"Error": "Pin not found"}, status=404)

        if pin.board.is_private and not request.user.is_superuser:
            if pin.board.owner != request.user:
                return Response({"Error": "Bummer you dont have access to this pin"})

        try:
            image = PinImage.objects.get(id=image_id)
        except PinImage.DoesNotExist:
            return Response({"Error": "Image not found"}, status=404)

        image.delete()
        return Response({"Message": "Image deleted successfully"}, status=200)

    def put(self, request, pin_id, image_id):
        try:
            pin = Pin.objects.get(id=pin_id)
        except Pin.DoesNotExist:
            return Response({"Error": "Pin not found"}, status=404)

        if pin.board.is_private and not request.user.is_superuser:
            if pin.board.owner != request.user:
                return Response({"Error": "Bummer you dont have access to this pin"})

        try:
            image = PinImage.objects.get(id=image_id)
        except PinImage.DoesNotExist:
            return Response({"Error": "Image not found"}, status=404)

        image.image = request.FILES['image']
        image.save()
        return Response({"Message": "Image updated successfully"}, status=200)

    def post(self, request, pin_id):
        try:
            pin = Pin.objects.get(id=pin_id)
        except Pin.DoesNotExist:
            return Response({"Error": "Pin not found"}, status=404)

        if pin.board.is_private and not request.user.is_superuser:
            if pin.board.owner != request.user:
                return Response({"Error": "Bummer you dont have access to this pin"})

        images = request.FILES.getlist('images')

        for image in images:
            PinImage.objects.create(pin=pin, image=image)

        return Response({"Message": "Image added successfully"}, status=201)
