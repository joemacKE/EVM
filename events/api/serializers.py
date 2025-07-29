from rest_framework import serializers
from events.models import Event
from django.conf import settings

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

class EventSerializer(serializers.ModelSerializer):
    #some basic validation
    def validate(self, data):
        #checks if start_date comes before end_date
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("The finish date cannot occur before the event is yet to start")


        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError("The event cannot be finished before it started")
        return data
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
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
    

    # #handles the updates
    # def update(self, instance,  **validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.start_date = validated_data.get('start_date', instance.start_date)
    #     instance.end_date = validated_data.get('end_date', instance.end_date)
    #     instance.start_time = validated_data.get('start_time', instance.start_time)
    #     instance.end_time = validated_data.get('end_time', instance.end_time)
    #     instance.is_public = validated_data.get('is_public', instance.is_public)
    #     instance.capacity = validated_data.get('capacity', instance.capacity)
    #     instance.category = validated_data.get('category', instance.category)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.location = validated_data.get('location', instance.location)
    #     instance.created_at = validated_data.get('created_at', instance.created_at)
    #     instance.updated_at = validated_data.get('updated_at', instance.updated_at)
    #     instance.save()
    #     return instance

