from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("games/", include("games.urls")),
    path("", include("users.urls")),
    path("health/", health_check, name="health"),
]

if settings.DEBUG:
    urlpatterns += [
        path("silk/", include("silk.urls", namespace="silk")),
    ]
