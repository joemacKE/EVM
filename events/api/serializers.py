from rest_framework import serializers
from events.models import Event, Comment
from django.conf import settings
from django.utils import timezone



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment", 'author', 'created_at']

class EventSerializer(serializers.ModelSerializer):
     comments = CommentSerializer(many=True, read_only= True)
     class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'organizer']


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
        
        def update(self, instance, validated_data):
            #overiding the update method to handle updates
            instance = super().update(instance, validated_data)
            return instance
    
    # def validate_organizer(self, value):
    #     if value != self.context['request'].user:
    #         raise serializers.ValidationError("You cannot create an event for another user")
    #     return value

# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookEvent
#         fields = "__all__"
#         read_only_fields = ['created_at', 'updated_at', 'payment_status' ]

#         def validate(self, data):
#             #checks if their is still slot for booking
#             if data['capacity']:
#                 ...
   
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fileds = ['id', 'comment', 'created_at']
        read_only_fields = ['created_at', 'updated_at']
        exclude = ['updated_at', 'id']

    
    def create(self, validate_data):
        return Event.objects.create(**validate_data)

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

