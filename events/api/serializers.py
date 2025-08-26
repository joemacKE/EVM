from rest_framework import serializers
from events.models import Event, Comment, BookEvent, Like
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime


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
        if value < timezone.now().date():
            raise serializers.ValidationError("The event cannot start in the past")
        return value

    def validate_capacity(self, value):
        if value < 10:
            raise serializers.ValidationError("You must have a minimum of 10 people for an event")
        return value

    def validate_is_paid(self, value):
        price = self.initial_data.get('price', 0)
        try:
            price = float(price)
        except (TypeError, ValueError):
            price = 0
        if value and price <= 0:
            raise serializers.ValidationError("If the event is paid, the price must be greater than 0")
        return value

    def validate_category(self, value):
        if value == 'select':
            raise serializers.ValidationError("Please select a valid event category")
        return value

    # --- Cross-field validation ---
    def validate(self, data):
    # Combine date + time to check full datetime
        start_datetime = datetime.combine(data['start_date'], data['start_time'])
        if start_datetime < timezone.now():
            raise serializers.ValidationError("The event cannot start in the past")

        # End datetime must be after start datetime
        end_datetime = datetime.combine(data['end_date'], data['end_time'])
        if end_datetime <= start_datetime:
            raise serializers.ValidationError("End date/time must be after start date/time")

        # Price rules
        if data.get('is_paid') and (data.get('price') is None or data['price'] <= 0):
            raise serializers.ValidationError("Paid events must have a price greater than 0.")
        if not data.get('is_paid') and data.get('price', 0) > 0:
            raise serializers.ValidationError("Free events cannot have a price.")

        return data

        
    def update(self, instance, validated_data):
        #overiding the update method to handle updates
        instance = super().update(instance, validated_data)
        return instance
    
    def create(self, validate_data):
        return Event.objects.create(**validate_data)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEvent
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at', 'payment_status', 'total_price']


    def create(self, validated_data):
            event = validated_data["event"]        # present because you passed it in save()
            tickets = validated_data.get("number_of_tickets", 1)

            # Build aware datetimes
            tz = timezone.get_current_timezone()
            event_start = timezone.make_aware(datetime.combine(event.start_date, event.start_time), tz)
            event_end   = timezone.make_aware(datetime.combine(event.end_date,   event.end_time),   tz)
            now = timezone.now()

            # Block anything that has started (change to `now > event_end` if you only want to block finished events)
            if now >= event_start:
                raise serializers.ValidationError("You cannot book an event that has already started or ended.")

            # Capacity based on existing bookings (more reliable than attendees M2M)
            already_booked = (
                BookEvent.objects.filter(event=event)
                .aggregate(total=Sum("number_of_tickets"))["total"] or 0
            )
            if already_booked + tickets > event.capacity:
                raise serializers.ValidationError("Not enough seats available for this booking.")

            # Payment rule
            if event.is_paid and validated_data.get("payment_status") == "unpaid":
                raise serializers.ValidationError("Paid events cannot be booked with unpaid status.")
            return BookEvent.objects.create(**validated_data)

                
                

   
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