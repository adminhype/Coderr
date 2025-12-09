import pytest

from django.urls import reverse

from offer_app.models import Offer, OfferDetail


@pytest.mark.django_db
def test_patch_offer_success_owner(api_client, business_user, offer):

    offer.details.all().delete()

    d1 = OfferDetail.objects.create(offer=offer, title="Old Basic", price=100.00,
                                    delivery_time_in_days=5, offer_type="basic")
    d2 = OfferDetail.objects.create(offer=offer, title="Old Premium", price=200.00,
                                    delivery_time_in_days=10, offer_type="premium")

    api_client.force_authenticate(user=business_user)

    payload = {
        "title": "New Title",
        "details": [
            {
                "offer_type": "basic",
                "price": 150.00,
                "title": "New Basic"
            }
        ]
    }

    url = reverse('offer-detail', kwargs={'pk': offer.id})
    response = api_client.patch(url, payload, format='json')

    assert response.status_code == 200

    offer.refresh_from_db()
    assert offer.title == "New Title"

    d1.refresh_from_db()
    assert d1.price == 150.00
    assert d1.title == "New Basic"

    assert d1.id == response.data['details'][0]['id']

    d2.refresh_from_db()
    assert d2.price == 200.00
    assert d2.title == "Old Premium"


@pytest.mark.django_db
def test_patch_offer_forbidden_not_owner(api_client, customer_user, offer):

    api_client.force_authenticate(user=customer_user)

    payload = {"title": "Hacked"}
    url = reverse('offer-detail', kwargs={'pk': offer.id})
    response = api_client.patch(url, payload, format='json')

    assert response.status_code == 403
