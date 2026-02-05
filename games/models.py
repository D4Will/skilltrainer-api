from django.db import models

class TargetScore(models.Model):
  time_elapsed = models.DurationField(null=False)
  clicks = models.IntegerField(null=False)
  targets = models.IntegerField(null=False)
  user = models.ForeignKey('users.User', on_delete=models.CASCADE)