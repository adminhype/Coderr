from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from profile_app.models import UserProfile
from profile_app.api.serializers import UserProfileSerializer


class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(UserProfile, user__pk=user_id)
