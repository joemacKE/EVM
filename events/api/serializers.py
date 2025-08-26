from rest_framework import serializers
from events.models import Event, Comment, BookEvent, Like
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, time


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
    status = serializers.SerializerMethodField()
    allow_booking = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_at', 'status', 'allow_booking', 'updated_at', 'organizer']

    def get_status(self, obj):
        return obj.current_status
    
    def get_allow_booking(self, obj):
        return obj.booking_allowed
        
    # --- Cross-field validation ---
    def validate(self, data):
        start_date = data.get("start_date")
        start_time = data.get("start_time")
        end_date = data.get("end_date")
        end_time = data.get("end_time")

        if isinstance(start_time, list):
            try:
                start_time = time(*map(int, start_time))  # e.g. ["14","40","00"] → 14:40:00
                data["start_time"] = start_time
            except Exception:
                raise serializers.ValidationError("Invalid start_time format")

        if isinstance(end_time, list):
            try:
                end_time = time(*map(int, end_time))
                data["end_time"] = end_time
            except Exception:
                raise serializers.ValidationError("Invalid end_time format")
    # Combine date + time to check full datetime
        start_dt = datetime.combine(start_date, start_time)
        end_dt = datetime.combine(end_date, end_time)
        if timezone.is_naive(start_dt):
            start_dt = timezone.make_aware(start_dt, timezone.get_current_timezone())
        if timezone.is_naive(end_dt):
            end_dt = timezone.make_aware(end_dt, timezone.get_current_timezone())

        # 🔹 Validation rules
        if start_dt < timezone.now():
            raise serializers.ValidationError("Event cannot start in the past")
        if end_dt <= start_dt:
            raise serializers.ValidationError("End date/time must be after start date/time")

        return data
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Event name must be at least 3 characters long.")
        return value

    def validate_start_date(self, value):
        now = timezone.localtime(timezone.now()).date()
        if value < now:
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