from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from accounts.models import CustomUser

CustomUser = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators = [validate_password])
    profile_pic = serializers.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = '__all__'
    

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username = validated_data['email'],
            email = validated_data['email'],
            salutation = validated_data['salutation'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phone_number = validated_data['salutation'],
            profile_pic = validated_data['profile_pic'],
            password = validated_data['password']
        

        )
        return user
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.salutation = validated_data.get('salutation', instance.salutation)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()
        return instance
        