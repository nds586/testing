from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from bookings.forms import BookingForm
from bookings.models import Booking
from users.models import Customer, ServiceProvider


@login_required
def create_booking(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = Customer.objects.get(user=request.user)
            booking.save()
            booking.assign_best_provider()
            return redirect('provider-discovery')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})


@login_required
def provider_invite_action(request: HttpRequest, booking_id: int, action: str) -> HttpResponse:
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(Booking, pk=booking_id)

    if booking.service_provider_id != provider.id:
        messages.error(request, 'This booking is not assigned to you.')
        return redirect('provider-workspace')

    if action == 'accept':
        booking.status = Booking.Status.ACCEPTED
        booking.save(update_fields=['status'])
        messages.success(request, 'Booking accepted.')
    elif action == 'reject':
        fallback = booking.handle_provider_rejection(rejecting_provider=provider)
        if fallback:
            messages.info(request, f'Booking reassigned to {fallback.user.email}.')
        else:
            messages.warning(request, 'No fallback provider is currently available.')
    elif action == 'start':
        booking.status = Booking.Status.STARTED
        booking.save(update_fields=['status'])
        messages.success(request, 'Booking started.')

    return redirect('provider-workspace')
