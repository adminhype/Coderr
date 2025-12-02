from rest_framework import serializers

from django.contrib.auth.models import User

from profile_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    def create(self, validated_data):
        user_type = validated_data.pop('type')
        password = validated_data.pop('password')
        validated_data.pop('repeated_password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, user_type=user_type)
        return user
