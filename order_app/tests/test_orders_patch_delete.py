import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from order_app.models import Order

User = get_user_model()


@pytest.mark.django_db
def test_patch_order_status_customer_user(api_client, customer_user, order_obj):

    api_client.force_authenticate(user=customer_user)

    payload = {
        "status": "completed"
    }

    url = f'/api/orders/{order_obj.id}/'
    response = api_client.patch(url, data=payload, format='json')

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_order_admin_user(api_client, admin_user, order_obj):

    api_client.force_authenticate(user=admin_user)

    url = f'/api/orders/{order_obj.id}/'
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_delete_order_business_forbidden(api_client, business_user, order_obj):

    api_client.force_authenticate(user=business_user)

    url = f'/api/orders/{order_obj.id}/'
    response = api_client.delete(url)

    assert response.status_code == 403
