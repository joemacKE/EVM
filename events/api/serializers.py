from rest_framework import serializers
from events.models import Event
from django.conf import settings
from django.utils import timezone



class EventSerializer(serializers.ModelSerializer):

    def validate_start_date(self, value):
        #checks if start_date comes before end_date
        if value < timezone.now().date():
            raise serializers.ValidationError("The event cannot start in the past")
        return value

    def validate(self, data):
        #checks if start_date is before end_date
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data
    
    def validate_capacity(self, value):
        #checks if capacity is greater than 10
        if value < 10:
            raise serializers.ValidationError("You must have a minimum of 10 people for an event")
        return value
    
    def validate_is_paid(self, value):
    # checks if is_paid is True, then price must be greater than 0
        price = self.initial_data.get('price', 0)
        try:
            price = float(price)
        except (TypeError, ValueError):
            price = 0
        if value and price <= 0:
            raise serializers.ValidationError("If the event is paid, the price must be greater than 0")
        return value
    
    def validate_category(self, value):
        #checks if category is selected
        try:
            if value == 'select':
                raise serializers.ValidationError("Please select a valid event category")
        except KeyError:
            raise serializers.ValidationError("Invalid Category selected")
        return value
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'organizer']

    
    def create(self, validate_data):
        return Event.objects.create(**validate_data)
    
    # name = serializers.CharField()
    # description = serializers.CharField()
    # start_date = serializers.DateField()
    # end_date = serializers.DateField()
    # start_time = serializers.TimeField()
    # end_time = serializers.TimeField()
    # is_public = serializers.BooleanField(default=False)
    # capacity = serializers.IntegerField(min_value=10)
    # category = serializers.CharField(choices=TYPE_OF_EVENT)
    # status = serializers.CharField(choices=STATUS_CHOICES)
    # image = serializers.ImageField(required=False)
    # location = serializers.CharField()
    # created_at = serializers.DateTimeField(read_only=True)
    # updated_at = serializers.DateTimeField(read_only=True)

    
    #basically returns all the objects
    # def get(self, validated_data):
    #     return Event.objects.create(**validated_data)
    

    #handles the updates
    def update(self, instance,  validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.category = validated_data.get('category', instance.category)
        instance.status = validated_data.get('status', instance.status)
        instance.image = validated_data.get('image', instance.image)
        instance.location = validated_data.get('location', instance.location)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.save()
        return instance

# TYPE_OF_EVENT = [
#         ('select', 'Select an Event'),
#         ('conference', 'Conference'),
#         ('webinar', 'Webinar'),
#         ('meet_and_greet', 'Meet and Greet'),
#         ('hackathon', 'Hackathon'),
#         ('coding_bootcamp', 'Coding BootCamp'),
#         ('movie_night', 'Movie Night'),
#         ('r_n_b_night', 'RnB Night'),
#         ('pack_and_chill', 'Pack and Chill'),
#         ('pack_and_grill', 'Pack and Grill'),
#         ('others', 'Others'),
#     ]
# STATUS_CHOICES = [
#         ('upcoming', 'Upcoming'),
#         ('ongoing', 'ongoing'),
#         ('cancelled', 'Cancelled'),
#         ('completed', 'Completed')
#     ]