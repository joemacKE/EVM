from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


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
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(10)], default=10)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    is_public = models.BooleanField(default=False)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Event: {self.name} Description: {self.description} Start Date: {self.start_date} Start Time: {self.start_time} Location: {self.location}"

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name = 'comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'author')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.author} commented on {self.event}: {self.comment[:20]}"
    #this model will define the relationship between events and users who comment on them

class Like(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')

    
# class BookEvent(models.Model):
#     BOOKING_STATUS = [
#         ('confirmed', 'Confirmed'),
#         ('pending', 'Pending'),
#         ('cancelled', 'Cancelled')
#     ]
#     PAYMENT_STATUS = [
#         ('select', 'Select Option'),
#         ('unpaid', 'Unpaid'),
#         ('paid', 'Paid'),
#         ('refunded', 'Refunded')
#     ]

#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='booking')
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,)
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='book_event')
#     booking_status = models.CharField(max_length=100, default='Pending', choices = BOOKING_STATUS)
#     number_of_tickets = models.PositiveIntegerField(default=1)
#     payment_status = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, choices=PAYMENT_STATUS)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     def save(self, *args, **kwargs):
#         if self.event.is_paid:
#             self.total_price = self.number_of_tickets * self.event.price
#         else:
#             self.total_price = 0.00
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.booking_status
    #this model will define the relationship between events and users who book them


