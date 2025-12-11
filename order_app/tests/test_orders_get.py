import pytest

from django.urls import reverse

from order_app.models import Order


@pytest.mark.django_db
def test_get_orders_as_customer(api_client, customer_user, business_user):

    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        title="my order",
        revisions=1,
        delivery_time_in_days=3,
        price=50.0,
        offer_type="basic",
        status="in_progress",
    )

    api_client.force_authenticate(user=customer_user)

    url = '/api/orders/'
    # url = reverse("orders-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == "my order"
    assert response.data[0]['customer'] == customer_user.id


@pytest.mark.django_db
def test_get_orders_as_business(api_client, customer_user, business_user):

    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        title="business job",
        revisions=1,
        delivery_time_in_days=1,
        price=100.0,
        offer_type="basic",
    )

    api_client.force_authenticate(user=business_user)

    url = '/api/orders/'
    # url = reverse("orders-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == "business job"
    assert response.data[0]['business'] == business_user.id


@pytest.mark.django_db
def test_get_orders_unauthenticated(api_client, user, customer_user, business_user):

    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        title="unauth user job",
        revisions=1,
        delivery_time_in_days=1,
        price=100.0,
        offer_type="basic",
    )

    api_client.force_authenticate(user=user)

    url = '/api/orders/'
    # url = reverse("orders-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0
