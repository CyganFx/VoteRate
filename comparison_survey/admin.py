from django.contrib import admin
from .models import *

# Register your models here.
# admin details : Comparison-manager - comparison
admin.site.register(ComparisonSurvey)
admin.site.register(RateObject)
admin.site.register(Complaint)
admin.site.register(ComparisonSurveyResult)
#admin.site.register(Roles)
admin.site.register(PassedSurvey)
