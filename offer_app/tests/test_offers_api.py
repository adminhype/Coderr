# import pytest

# # from django.urls import reverse


# @pytest.mark.django_db
# def test_get_offers_list(api_client, offer, offer_detail):
#     # url = reverse('offers-list')
#     url = "/api/offers/"
#     response = api_client.get(url)

#     assert response.status_code == 200
#     data = response.data['results'][0]

#     assert data['title'] == offer.title
#     assert data['min_price'] == 100.00
#     assert data['min_delivery_time'] == 5
#     assert 'details' in data
#     assert 'url' in data['details'][0]
#     assert 'user_details' in data
