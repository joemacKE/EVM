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
        profile_pic = validated_data.get('profile_pic', None)
        user = CustomUser.objects.create_user(
            username = validated_data['email'],
            email = validated_data['email'],
            salutation = validated_data['salutation'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phone_number = validated_data['salutation'],
            password = validated_data['password']
        

        )
        return user
        