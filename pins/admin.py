from django.contrib import admin
from .models import Pin, Pin_Board, PinImage


# Register your models here.
class PinAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','board','board_id', 'description', 'created_at', 'updated_at']
    search_fields = ['title', 'board', 'description']
    list_filter = ['board', 'created_at', 'updated_at']
    list_per_page = 10


admin.site.register(Pin, PinAdmin)


class Pin_BoardAdmin(admin.ModelAdmin):
    list_display = ['id', 'pin', 'board', 'board_id']
    search_fields = ['pin', 'board']
    list_filter = ['pin', 'board', 'created_at', 'updated_at']


admin.site.register(Pin_Board, Pin_BoardAdmin)


class PinImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'pin', 'pin_id', 'image']
    search_fields = ['pin', 'image']
    list_filter = ['pin']


admin.site.register(PinImage, PinImageAdmin)
