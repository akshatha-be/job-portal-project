from django.contrib import admin
from .models import Job, Application, UserProfile

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'category', 'job_type', 'employer', 'created_at', 'is_active')
    list_filter = ('category', 'job_type', 'is_active')
    search_fields = ('title', 'company', 'location')
    list_editable = ('is_active',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('applicant__username', 'job__title')
    list_editable = ('status',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)
