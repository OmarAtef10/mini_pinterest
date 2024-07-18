from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from boards.models import Board


# Create your models here.
class Pin(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='pins') #moved to a separate model to handel multiple images
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PinImage(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pins')

    def __str__(self):
        return self.pin.title


# @receiver(post_save, sender=Pin)
# def create_pin_board(sender, instance, created, **kwargs):
#     if created:
#         try:
#             Pin_Board.objects.create(pin=instance, board=instance.board)
#         except Exception as e:
#             print(e)
#             Pin.objects.delete(instance) # commented bc i want to see the error and return a response


class Pin_Board(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pin.title} - {self.board.name}'

    class Meta:
        unique_together = ('pin', 'board')
