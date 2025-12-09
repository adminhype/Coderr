import pytest

from django.urls import reverse

from offer_app.models import Offer, OfferDetail


@pytest.mark.django_db
def test_get_offer_detail(api_client, business_user, offer):
    OfferDetail.objects.create(offer=offer, title="Basic", price=100.00,
                               delivery_time_in_days=5, features=["A"], offer_type="basic")
    OfferDetail.objects.create(offer=offer, title="Premium", price=200.00,
                               delivery_time_in_days=7, features=["B"], offer_type="premium")

    api_client.force_authenticate(user=business_user)

    url = reverse('offer-detail', kwargs={'pk': offer.id})
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.data

    assert data['id'] == offer.id
    assert data['title'] == offer.title

    assert data['min_price'] == 100.00
    assert data['min_delivery_time'] == 5

    assert 'user_details' not in data

    assert 'user' in data
    assert data['user'] == business_user.id

    assert len(data['details']) == 2
    first_url = data['details'][0]['url']
    assert 'http' in first_url
    assert '/api/offerdetails/' in first_url


@pytest.mark.django_db
def test_get_offer_detail_unauthorized(api_client, offer):
    url = reverse('offer-detail', kwargs={'pk': offer.id})
    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_get_offer_detail_not_found(api_client, business_user):
    api_client.force_authenticate(user=business_user)

    url = reverse('offer-detail', kwargs={'pk': 2025})
    response = api_client.get(url)

    assert response.status_code == 404
