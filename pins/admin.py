from django.contrib import admin
from .models import Pin, Pin_Board, PinImage


# Register your models here.
class PinAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'created_at', 'updated_at']
    search_fields = ['title', 'board', 'description']
    list_filter = ['board', 'created_at', 'updated_at']
    list_per_page = 10


admin.site.register(Pin, PinAdmin)
admin.site.register(Pin_Board)
admin.site.register(PinImage)
