# core/admin.py
from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'service', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'rating', 'service')
    search_fields = ('name', 'content', 'company')
    actions = ['approve_testimonials', 'reject_testimonials'] # Custom admin actions

    # Fields that can be edited in the admin change form
    fields = (
        'name', 'position', 'company', 'email', 'rating', 'content', 'service',
        'approved', # This field should be editable by admin
        'created_at', 'updated_at'
    )
    readonly_fields = ('created_at', 'updated_at') # These fields are not editable

    def approve_testimonials(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected testimonials have been approved.")
    approve_testimonials.short_description = "Approve selected testimonials"

    def reject_testimonials(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected testimonials have been rejected (unapproved).")
    reject_testimonials.short_description = "Reject selected testimonials"

    # Optionally, you can override `has_add_permission` if you don't want admins to manually add testimonials directly
    # def has_add_permission(self, request):
    #     return False # If you want all testimonials to come through the frontend form only

    # Optionally, prevent direct deletion from admin if preferred, but allow unapproving
    # def has_delete_permission(self, request, obj=None):
    #     return False
