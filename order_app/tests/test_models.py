import pytest

from order_app.models import Order

from offer_app.models import OfferDetail


@pytest.mark.django_db
def test_order_creation_snapshot(customer_user, business_user, offer_detail):
    order = Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        title=offer_detail.title,
        revisions=offer_detail.revisions,
        delivery_time_in_days=offer_detail.delivery_time_in_days,
        price=offer_detail.price,
        features=offer_detail.features,
        offer_type=offer_detail.offer_type,
        status='in_progress'
    )

    assert order.title == offer_detail.title
    assert order.price == offer_detail.price
    assert order.customer_user == customer_user
    assert order.business_user == business_user
    assert order.status == 'in_progress'
    assert str(order) == offer_detail.title


@pytest.mark.django_db
def test_order_status_choices(customer_user, business_user):
    order = Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        title="Test",
        revisions=1,
        delivery_time_in_days=1,
        price=10.00,
        features=[],
        offer_type="basic",
        status="completed"
    )
    assert order.status == "completed"
