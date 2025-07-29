from rest_framework import serializers
from events.models import Event
from django.conf import settings

TYPE_OF_EVENT = [
        ('select', 'Select an Event'),
        ('conference', 'Conference'),
        ('webinar', 'Webinar'),
        ('meet_and_greet', 'Meet and Greet'),
        ('hackathon', 'Hackathon'),
        ('coding_bootcamp', 'Coding BootCamp'),
        ('movie_night', 'Movie Night'),
        ('r_n_b_night', 'RnB Night'),
        ('pack_and_chill', 'Pack and Chill'),
        ('pack_and_gril', 'Pack and Grill'),
        ('others', 'Others'),
    ]
STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'ongoing'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]
class EventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    is_public = serializers.BooleanField(default=False)
    capacity = serializers.IntegerField(min_value=10)
    category = serializers.CharField(max_length=120, choices=TYPE_OF_EVENT)
    status = serializers.CharField(max_length=120, choices=STATUS_CHOICES)
    image = serializers.ImageField(required=False)
    location = serializers.CharField(max_length=200)
    created_at = serializers.DateTimeField(auto_now_add=True)
    updated_at = serializers.DateTimeField(auto_now=True)
