from django.contrib import admin

from bookings.models import Booking, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'service_provider', 'category', 'scheduledTime', 'status')
    list_filter = ('status', 'category')
    search_fields = ('customer__user__email', 'service_provider__user__email')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != Booking.Status.PENDING:
            return ('service_provider',)
        return ()


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating')
    search_fields = ('booking__customer__user__email', 'booking__service_provider__user__email')
