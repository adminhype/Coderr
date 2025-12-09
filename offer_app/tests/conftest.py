import pytest

from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from offer_app.models import Offer, OfferDetail
from profile_app.models import UserProfile


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def business_user():
    user = User.objects.create_user(
        username='bob', password='123', email='bob@example.com')
    UserProfile.objects.create(user=user, user_type='business')
    return user


@pytest.fixture
def customer_user():
    user = User.objects.create_user(
        username='morty', password='123', email='morty@example.com')
    UserProfile.objects.create(user=user, user_type='customer')
    return user


@pytest.fixture
def offer(business_user):
    return Offer.objects.create(user=business_user, title="test offer", description="desc")


@pytest.fixture
def offer_detail(offer):
    return OfferDetail.objects.create(offer=offer, title="basic", revisions=1, delivery_time_in_days=5, price=100, features=['A'], offer_type="basic")
