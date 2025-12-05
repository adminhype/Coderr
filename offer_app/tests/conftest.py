import pytest

from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from offer_app.models import Offer, OfferDetail


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username='bob', password='123')


@pytest.fixture
def offer(user):
    return Offer.objects.create(user=user, title="test offer", description="desc")


@pytest.fixture
def offer_detail(offer):
    return OfferDetail.objects.create(offer=offer, title="basic", revisions=1, delivery_time_in_days=5, price=100, features=['A'], offer_type="basic")
