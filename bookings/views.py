from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from bookings.forms import BookingForm
from users.models import Customer


@login_required
def create_booking(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = Customer.objects.get(user=request.user)
            booking.save()
            return redirect('booking-create')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})
