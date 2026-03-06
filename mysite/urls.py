from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('games/', include('games.urls')),
    path('', include('users.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
]
