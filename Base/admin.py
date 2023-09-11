from django.contrib import admin
from .models import Submission, Grading, AccessCode

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'state_of_origin', 'current_level')
    list_filter = ('state_of_origin', 'current_level')
    search_fields = ('name', 'state_of_origin', 'educational_institution')

class GradingAdmin(admin.ModelAdmin):
    list_display = ('submission', 'grade')
    list_filter = ('grade',)

class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'used')
    list_filter = ('used',)
    search_fields = ('code',)
    ordering = ('-id',)  # Order by creation date (or any other field you prefer)

admin.site.register(AccessCode, AccessCodeAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Grading, GradingAdmin)
