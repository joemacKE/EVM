from django.contrib import admin
from .models import Event, Comment, Notification

admin.site.register(Event)
# @admin.register(BookEvent)
# class BookEventAdmin(admin.ModelAdmin):
#     list_display = ('id', 'event', 'user', 'number_of_tickets', 'payment_status', 'created_at', 'updated_at')
#     search_fields = ('author', 'event', 'payment_status')
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'event', 'comment', 'created_at', 'updated_at')
    search_fields = ('author__username', 'comment', 'event__title')
# Register your models here.
