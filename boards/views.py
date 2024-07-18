from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from boards.models import Board
from boards.serializers import BoardSerializer


# Create your views here.
class ManageBoardView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        board = get_object_or_404(self.queryset, pk=self.kwargs['pk'])
        if self.request.user.is_superuser:
            return board

        if not board.owner == self.request.user:
            self.permission_denied(self.request)
        return board


class ListCreateBoardView(ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
