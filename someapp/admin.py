from django.contrib import admin
from .models import Profile, Application, Review

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'email')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transport', 'start_date', 'payment', 'status')
    list_filter = ('status', 'transport', 'payment')
    search_fields = ('user__username', 'user__profile__full_name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'rating', 'created_at')