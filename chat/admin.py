from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "content", "timestamp")
    list_filter = ("room",)
    search_fields = ("content",)
