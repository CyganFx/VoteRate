from django.contrib import admin
from .models import *


# Register your models here.
# admin details : Comparison-manager - comparison

@admin.register(ComparisonSurvey)
class ComparisonSurveyAdmin(admin.ModelAdmin):
    list_display = ('topic', 'category', 'rating')
    list_filter = ('category',)
    search_fields = ('topic', 'description',)


admin.site.site_header = 'VoteRate Admin Panel'

admin.site.register(Category)
admin.site.register(RateObject)
admin.site.register(Complaint)
admin.site.register(ComparisonSurveyResult)
admin.site.register(PassedSurvey)
