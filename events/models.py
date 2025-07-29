from django.db import models
from django.conf import settings


class Event(models.Model):
    TYPE_OF_EVENT = [
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
    oganizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_public = models.BooleanField(default=False)
    capacity = models.PositiveIntegerField()
    category = models.CharField(max_length=120, choices=TYPE_OF_EVENT)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to='images/')


    location = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)



# Create your models here.
