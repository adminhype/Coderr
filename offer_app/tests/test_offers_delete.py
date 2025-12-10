import pytest
from django.urls import reverse
from offer_app.models import Offer


@pytest.mark.django_db
def test_delete_offer_success_owner(api_client, business_user, offer):
    api_client.force_authenticate(user=business_user)

    url = reverse('offer-detail', kwargs={'pk': offer.id})
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Offer.objects.count() == 0


@pytest.mark.django_db
def test_delete_offer_forbidden_not_owner(api_client, customer_user, offer):
    api_client.force_authenticate(user=customer_user)

    url = reverse('offer-detail', kwargs={'pk': offer.id})
    response = api_client.delete(url)

    assert response.status_code == 403
    assert Offer.objects.count() == 1
