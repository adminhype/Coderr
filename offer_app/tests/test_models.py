import pytest

from offer_app.models import Offer, OfferDetail


@pytest.mark.django_db
def test_offer_string_representation(offer):
    assert str(offer) == offer.title


@pytest.mark.django_db
def test_offer_relation(user):
    offer = Offer.objects.create(
        user=user,
        title="Test Offer",
        description="Description"
    )
    assert offer.user == user
    assert user.offers.count() == 1


@pytest.mark.django_db
def test_offer_detail_creation(offer):
    features_list = ["Logo", "Design"]
    detail = OfferDetail.objects.create(
        offer=offer,
        title="Premium",
        revisions=3,
        delivery_time_in_days=7,
        price=199.99,
        features=features_list,
        offer_type="premium"
    )

    assert detail.title == "Premium"
    assert detail.features == features_list
    assert detail.price == 199.99
    assert offer.details.count() == 1
    assert str(detail) == "Premium (premium)"


@pytest.mark.django_db
def test_offer_ordering(user):
    offer1 = Offer.objects.create(user=user, title="Old", description="D")
    offer2 = Offer.objects.create(user=user, title="New", description="D")

    assert Offer.objects.first() == offer2
