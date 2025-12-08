import django_filters

from offer_app.models import Offer


class OfferFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='min_price', lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(
        field_name='max_delivery_time', lookup_expr='lte')
    creator_id = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']
