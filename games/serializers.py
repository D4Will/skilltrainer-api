from rest_framework import serializers
from games.models import TargetScore

class TargetScoreSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(read_only=True)
  
  class Meta:
    model = TargetScore
    fields = [
      'id',
      'time_elapsed',
      'clicks',
      'targets',
      'user',
    ]
