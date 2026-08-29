from django.contrib import admin
from games.models import TargetScore, ReactionScore, TypingScore

admin.site.register([TargetScore, ReactionScore, TypingScore])
