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


class OfferDetailAbsoluteSerializer(OfferDetailSerializer):
    def get_url(self, obj):

        path = f"/api/offerdetails/{obj.id}/"
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(path)
        return path


class OfferDetailDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]


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


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailDataSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details',
        ]

    def validate_details(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "At least 3 offer details are required.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer


class OfferRetrieveSerializer(serializers.ModelSerializer):
    details = OfferDetailAbsoluteSerializer(many=True, read_only=True)
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
        ]


class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]
        extra_kwargs = {
            'title': {'required': False},
            'revisions': {'required': False},
            'delivery_time_in_days': {'required': False},
            'price': {'required': False},
            'features': {'required': False},
            'offer_type': {'required': True},
        }


class OfferUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details',
        ]

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.image = validated_data.get('image', instance.image)

        instance.save()

        details_data = validated_data.get('details')
        if details_data:
            for detail_input in details_data:
                offer_type = detail_input.get('offer_type')
                try:
                    detail_obj = instance.details.get(offer_type=offer_type)
                    if 'title' in detail_input:
                        detail_obj.title = detail_input['title']
                    if 'revisions' in detail_input:
                        detail_obj.revisions = detail_input['revisions']
                    if 'delivery_time_in_days' in detail_input:
                        detail_obj.delivery_time_in_days = detail_input['delivery_time_in_days']
                    if 'price' in detail_input:
                        detail_obj.price = detail_input['price']
                    if 'features' in detail_input:
                        detail_obj.features = detail_input['features']
                    detail_obj.save()
                except OfferDetail.DoesNotExist:
                    pass
        return instance
