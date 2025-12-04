from rest_framework import serializers

from django.contrib.auth.models import User

from profile_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    type = serializers.CharField(source='user_type', read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')

        user = instance.user

        if email:
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                raise serializers.ValidationError(
                    {"email": "Email already exist."})

        user.email = email
        user.save()

        return super().update(instance, validated_data)


class BusinessProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username', read_only=True)
    type = serializers.CharField(source='user_type', read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
        ]


class CustomerProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username', read_only=True)
    type = serializers.CharField(source='user_type', read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'type'
        ]
