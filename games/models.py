from django.db import models
from django.contrib.postgres.fields import ArrayField

class TargetScore(models.Model):
  time_elapsed = models.DurationField(null=False)
  clicks = models.PositiveSmallIntegerField(null=False)
  targets = models.PositiveSmallIntegerField(null=False)
  user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)

class ReactionScore(models.Model):
  reaction_times = ArrayField(models.PositiveSmallIntegerField(), null=False)
  user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)

class TypingScore(models.Model):
  wpm = models.PositiveSmallIntegerField(null=False)
  accuracy = models.DecimalField(null=False, max_digits=4, decimal_places=1)
  raw_wpm = models.PositiveSmallIntegerField(null=False)
  time_mode = models.PositiveSmallIntegerField(null=False)
  user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)