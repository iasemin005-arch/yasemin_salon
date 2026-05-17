from django.contrib import admin
from .models import Service, Master, GalleryPhoto, Review, Appointment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    list_editable = ['price', 'is_active', 'order']
    search_fields = ['name']


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'experience_years', 'is_active']
    list_editable = ['is_active']


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'master', 'uploaded_at', 'is_active']
    list_filter = ['category', 'is_active', 'master']
    list_editable = ['is_active']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'rating', 'service', 'created_at', 'is_approved']
    list_filter = ['rating', 'is_approved']
    list_editable = ['is_approved']
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = 'Одобрить выбранные отзывы'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_phone', 'service', 'master', 'date', 'time', 'status', 'payment_method', 'is_paid']
    list_filter = ['status', 'payment_method', 'is_paid', 'date']
    list_editable = ['status', 'is_paid']
    search_fields = ['client_name', 'client_phone']
    date_hierarchy = 'date'
