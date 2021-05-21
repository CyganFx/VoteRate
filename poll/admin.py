from django.contrib import admin

from .models import *

admin.site.register(Poll)
admin.site.register(PollQuestion)
admin.site.register(PollAnswer)
admin.site.register(PollVote)
admin.site.register(Category)
admin.site.register(UserPollRatings)
admin.site.register(PollStats)

