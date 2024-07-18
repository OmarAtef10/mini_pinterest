from django.contrib import admin
from .models import Board


# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'owner', 'is_private', 'created_at', 'updated_at')
    list_filter = ('is_private',)
    search_fields = ('name', 'owner__username')
    ordering = ('-created_at',)


admin.site.register(Board, BoardAdmin)
