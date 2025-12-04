from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from profile_app.models import UserProfile
from profile_app.api.serializers import BusinessProfileListSerializer, CustomerProfileListSerializer, UserProfileSerializer
from profile_app.api.permissions import isOwnerOrReadOnly


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, isOwnerOrReadOnly]

    def get_object(self):
        user_id = self.kwargs.get('pk')
        obj = get_object_or_404(UserProfile, user__pk=user_id)

        self.check_object_permissions(self.request, obj)
        return obj


class BusinessProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(user_type='business')
    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


class CustomerProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(user_type='customer')
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
