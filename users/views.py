from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class UserProfileView(APIView):
    def get(self, request):
        return Response({
            "username": request.user.username,
            "groups": list(request.user.groups.values_list("name", flat=True))  # ✅ group names
        }) 