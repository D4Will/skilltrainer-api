from django.urls import path
from games import views

urlpatterns = [
  path('target-scores/', views.TargetScoreListCreateView.as_view()),
  path('target-average/', views.TargetScoreAggregateView.as_view())
]