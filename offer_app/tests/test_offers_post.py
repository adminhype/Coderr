import pytest

from django.urls import reverse

from offer_app.models import Offer


@pytest.mark.django_db
def test_create_offer_as_business_user(api_client, business_user):
    api_client.force_authenticate(user=business_user)

    payload = {
        "title": "new graphic design",
        "description": "Description...",
        "details": [
            {
                "title": "Basic",
                "revisions": 1,
                "delivery_time_in_days": 5,
                "price": 50.00,
                "features": ["Feature A"],
                "offer_type": "basic"
            },
            {
                "title": "Standard",
                "revisions": 2,
                "delivery_time_in_days": 3,
                "price": 100.00,
                "features": ["Feature A", "Feature B"],
                "offer_type": "standard"
            },
            {
                "title": "Premium",
                "revisions": 3,
                "delivery_time_in_days": 1,
                "price": 150.00,
                "features": ["All"],
                "offer_type": "premium"
            }
        ]
    }

    url = reverse('offer-list')
    response = api_client.post(url, payload, format='json')

    assert response.status_code == 201
    assert Offer.objects.count() == 1
    assert Offer.objects.first().user == business_user


@pytest.mark.django_db
def test_create_offer_as_customer_user(api_client, customer_user):
    api_client.force_authenticate(user=customer_user)

    payload = {
        "title": "new graphic design",
        "description": "Description",
        "details": []
    }

    url = reverse('offer-list')
    response = api_client.post(url, payload, format='json')

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_offer_validation_details_count(api_client, business_user):
    api_client.force_authenticate(user=business_user)

    payload = {
        "title": "new graphic design",
        "description": "...",
        "details": [
            {
                "title": "Only one",
                "revisions": 1,
                "delivery_time_in_days": 5,
                "price": 50.00,
                "features": [],
                "offer_type": "basic"
            }
        ]
    }
    url = reverse('offer-list')
    response = api_client.post(url, payload, format='json')

    assert response.status_code == 400
    assert Offer.objects.count() == 0
