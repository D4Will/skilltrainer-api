from rest_framework import serializers
from games.models import TargetScore, ReactionScore, TypingScore

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

  def validate(self, data):
    if data['clicks'] < data['targets']:
      raise serializers.ValidationError('Clicks cannot be less than targets.')
    if data['targets'] not in [15, 30, 45]:
      raise serializers.ValidationError('Incorrect target amount.')
    return data


class ReactionScoreSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(read_only=True)

  class Meta:
    model = ReactionScore
    fields = [
      'id', 
      'reaction_times',
      'user',
    ]

  def validate(self, data):
    for time in data['reaction_times']:
      if time < 0:
        raise serializers.ValidationError('Times must be positive.')
    return data


class TypingScoreSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(read_only=True)

  class Meta:
    model = TypingScore
    fields = [
      'id', 
      'wpm',
      'accuracy',
      'raw_wpm',
      'time_mode',
      'user',
    ]
  
  def validate(self, data):
    if data['wpm'] < 0:
      raise serializers.ValidationError('wpm must be positive.')
    if data['accuracy'] < 0:
      raise serializers.ValidationError('accuracy must be positive.')
    if data['raw_wpm'] < 0:
      raise serializers.ValidationError('raw_wpm must be positive.')
    if data['time_mode'] not in [15,30,60]:
      raise serializers.ValidationError('Incorrect Time Mode.')
    return data