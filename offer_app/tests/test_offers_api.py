import pytest

from django.urls import reverse

from offer_app.models import Offer, OfferDetail


@pytest.mark.django_db
def test_get_offers_list_strucutre(api_client, user):
    offer = Offer.objects.create(
        user=user, title="web development", description="deploy a website")

    OfferDetail.objects.create(offer=offer, title="frontend", offer_type="premium", price=500.00, features=[
                               "angular", "scss"], delivery_time_in_days=15, revisions=2)
    OfferDetail.objects.create(offer=offer, title="backend", offer_type="basic", price=30.00, features=[
                               "django", "rest"], delivery_time_in_days=30, revisions=5)

    url = reverse('offer-list')
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.data['results'][0]

    assert data['min_price'] == 30.00
    assert data['min_delivery_time'] == 15

    assert data['user_details']['username'] == user.username

    assert len(data['details']) == 2
    assert 'id' in data['details'][0]
    assert 'url' in data['details'][0]

    assert '/offerdetails/' in data['details'][0]['url']


@pytest.mark.django_db
def test_get_offer_filter_min_price(api_client, user):
    offer1 = Offer.objects.create(
        user=user, title="web development", description="deploy a website")
    OfferDetail.objects.create(offer=offer1, title="frontend", offer_type="basic", price=50.00, features=[
                               "angular", "scss"], delivery_time_in_days=15, revisions=2)

    offer2 = Offer.objects.create(
        user=user, title="backend development", description="fast api")
    OfferDetail.objects.create(offer=offer2, title="backend", offer_type="premium", price=300.00, features=[
                               "django", "rest"], delivery_time_in_days=30, revisions=5)

    response = api_client.get('/api/offers/?min_price=100')

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['id'] == offer2.id
