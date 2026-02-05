from rest_framework import serializers
from games.models import TargetScore

class TargetScoreSerializer(serializers.ModelSerializer):
  class Meta:
    model = TargetScore
    fields = [
      'time_elapsed',
      'clicks',
      'targets',
      'user',
    ]