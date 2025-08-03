from django.db import models
from django.conf import settings


class Event(models.Model):
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
        ('pack_and_grill', 'Pack and Grill'),
        ('others', 'Others'),
    ]
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'ongoing'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=120, choices=TYPE_OF_EVENT)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=120, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    is_public = models.BooleanField(default=False)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Event: {self.name} Description: {self.description} Start Date: {self.start_date} Start Time: {self.start_time} Location: {self.location}"



# Create your models here.
