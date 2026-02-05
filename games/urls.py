from django.urls import path
from games import views

urlpatterns = [
  path('target-scores/', views.TargetScoreListCreateView.as_view()),
  path('target-scores/<int:score_id>', views.TargetScoreDetailAPIView.as_view()),
]