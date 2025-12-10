import pytest

from django.urls import reverse

from offer_app.models import OfferDetail


@pytest.mark.django_db
def test_get_offer_detail_single_success(api_client, customer_user, offer_detail):
    api_client.force_authenticate(user=customer_user)

    url = reverse('offerdetail-detail', kwargs={'pk': offer_detail.id})
    # url = ('/api/offerdetails/{}/').format(offer_detail.id)
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.data

    assert data['id'] == offer_detail.id
    assert data['title'] == offer_detail.title
    assert float(data['price']) == float(offer_detail.price)
    assert data['offer_type'] == offer_detail.offer_type


@pytest.mark.django_db
def test_get_offer_detail_single_unauthorized(api_client, offer_detail):
    url = reverse('offerdetail-detail', kwargs={'pk': offer_detail.id})
    # url = ('/api/offerdetails/{}/').format(offer_detail.id)
    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_get_offer_detail_single_not_found(api_client, customer_user):
    api_client.force_authenticate(user=customer_user)

    url = reverse('offerdetail-detail', kwargs={'pk': 28755})
    # url = ('/api/offerdetails/{}/').format(28755)
    response = api_client.get(url)

    assert response.status_code == 404
