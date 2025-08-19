from django.contrib import admin
from .models import Event, Comment, BookEvent, Notification

admin.site.register(Event)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'event', 'comment', 'created_at', 'updated_at')
    search_fields = ('author__username', 'comment', 'event__title')
# Register your models here.
