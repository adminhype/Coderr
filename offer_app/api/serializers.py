from rest_framework import serializers

from django.contrib.auth import get_user_model

from offer_app.models import Offer, OfferDetail

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)
    user_details = UserDetailSerializer(source='user', read_only=True)
    min_price = serializers.FloatField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details',
        ]
