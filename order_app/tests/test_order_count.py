import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from order_app.models import Order

User = get_user_model()


@pytest.mark.django_db
def test_get_order_count(api_client, customer_user, business_user, order_obj):

    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        title='old order',
        revisions=1,
        delivery_time_in_days=3,
        price=50,
        offer_type='basic',
        status="completed"
    )

    api_client.force_authenticate(user=customer_user)

    url = reverse('order-count', kwargs={'business_user_id': business_user.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['order_count'] == 1


@pytest.mark.django_db
def test_get_order_count_unauthorized(api_client, business_user):

    url = reverse('order-count', kwargs={'business_user_id': business_user.id})
    response = api_client.get(url)

    assert response.status_code == 401
