from django.urls import path
from games import views

urlpatterns = [
  path('target-scores/', views.TargetScoreListCreateView.as_view()),
  path('target-average/', views.TargetScoreAggregateView.as_view()),
  path('reaction-scores/', views.ReactionScoreListCreateView.as_view()),
  path('reaction-average/', views.ReactionScoreAggregateView.as_view()),
  path('typing-scores/', views.TypingScoreListCreateView.as_view()),
  path('typing-average/', views.TypingScoreAggregateView.as_view()),
]