from django.urls import path
from users import views

urlpatterns = [
  path('register/', views.RegularUserView.as_view()),
  path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
  path('logout/', views.LogoutView.as_view()),
  path('authenticated/', views.IsAuthenticatedView.as_view()),
]