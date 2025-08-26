from rest_framework import serializers
from events.models import Event, Comment, BookEvent, Like
from django.conf import settings
from django.utils import timezone



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # shows username instead of ID
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "comment", "author", "event", "created_at", "updated_at"]
    
    def validate_comment(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        return value

class EventSerializer(serializers.ModelSerializer):
     comments = CommentSerializer(many=True, read_only= True)
     class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'organizer']

        def validate_name(self, value):
            if len(value) < 3:
                raise serializers.ValidationError("Event name must be at least 3 characters long.")
            return value
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
        def validate(self, data):
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError("ENd time must be after start time")
            return data
        def validate(self, data):
            if data.get('is_paid') and (data.get('price')is None or data['price'] <= 0):
                raise serializers.ValidationError("Paid events must have aprice greater than 0.")
            if not data.get('is_paid') and data.get('price', 0) > 0:
                raise serializers.ValidationError('Free events cannot have a price.')
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
    
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEvent
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at', 'payment_status', 'total_price']

        def validate(self, data):
            event = data['event']
            #checks if their is still slot for booking
            tickets_requested = data.get('number_of_tickets', 1)
            if event.attendees.count() + tickets_requested > event.capacity:
                raise serializers.ValidationError('This event is fully booked')
            return data
        
        def validate(self, data):
            event = data['event']
            tickets = data['number_of_tickets']
            if event.attendees.count() + tickets > event.capacity:
                raise serializers.ValidationError("Not enough slots for this booking")
            return data
        
        def validate(self, data):
            if data['event'].is_paid and data['payment_status'] == "unpaid":
                raise serializers.ValidationError("Paid events cannot be booked with unpaid status")
            return data
        



                
                

    
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

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"