import pytest

from django.urls import reverse

from order_app.models import Order

from profile_app.models import UserProfile


@pytest.mark.django_db
def test_create_order(api_client, customer_user, business_user, offer_detail):

    api_client.force_authenticate(user=customer_user)

    payload = {
        'offer_detail_id': offer_detail.id,
    }

    url = reverse('order-list')
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == 201

    assert Order.objects.count() == 1
    new_order = Order.objects.first()

    assert new_order.title == offer_detail.title
    assert new_order.price == offer_detail.price
    assert new_order.business_user == business_user
    assert new_order.customer_user == customer_user
    assert new_order.status == 'in_progress'


@pytest.mark.django_db
def test_create_order_forbidden_for_business_user(api_client, business_user, offer_detail):

    api_client.force_authenticate(user=business_user)

    payload = {
        'offer_detail_id': offer_detail.id,
    }

    url = reverse('order-list')
    response = api_client.post(url, data=payload, format='json')

    assert business_user.profile.user_type == 'business'
    assert response.status_code == 403
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_create_order_invalid_id(api_client, customer_user):

    api_client.force_authenticate(user=customer_user)

    payload = {
        'offer_detail_id': 11122025,
    }
    url = reverse('order-list')
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code in [400, 404]
