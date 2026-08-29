from rest_framework import status
from rest_framework.views import APIView
from users.serializers import RegularUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin
from datetime import timedelta

from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

samesite_setting = settings.COOKIE_SAMESITE
domain_setting = settings.COOKIE_DOMAIN


class RegularUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegularUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            access_token = tokens["access"]
            refresh_token = tokens["refresh"]

            res = Response()
            res.data = {"success": True}

            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite=samesite_setting,
                path="/",
                domain=domain_setting,
                max_age=timedelta(hours=1),
            )

            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite=samesite_setting,
                path="/",
                domain=domain_setting,
                max_age=timedelta(weeks=99),
            )

            return res

        except:
            return Response({"success": False})


class CustomTokenRefreshView(TokenRefreshView, BlacklistMixin):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            RefreshToken(refresh_token).check_blacklist()

            request.data["refresh"] = refresh_token
            response = super().post(request, *args, **kwargs)

            tokens = response.data
            access_token = tokens["access"]

            res = Response()
            res.data = {"refreshed": True}

            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite=samesite_setting,
                path="/",
                domain=domain_setting,
                max_age=timedelta(hours=1),
            )

            return res

        except:
            return Response({"refreshed": False})


class LogoutView(APIView, BlacklistMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            RefreshToken(refresh_token).blacklist()

            res = Response()
            res.data = {"success": True}

            res.set_cookie(
                key="access_token",
                value=None,
                httponly=True,
                secure=True,
                samesite=samesite_setting,
                path="/",
                domain=domain_setting,
                max_age=timedelta(seconds=1),
            )

            res.set_cookie(
                key="refresh_token",
                value=None,
                httponly=True,
                secure=True,
                samesite=samesite_setting,
                path="/",
                domain=domain_setting,
                max_age=timedelta(seconds=1),
            )
            return res
        except:
            return Response({"success": False})


class IsAuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"authenticated": True, "name": request.user.username})
