from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q, Sum
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from bookings.models import Booking, Review
from services.models import ServiceCategory
from users.models import Customer, ServiceProvider


def hero_landing(request: HttpRequest) -> HttpResponse:
    return render(request, 'vibe/index.html')


def service_discovery(request: HttpRequest) -> HttpResponse:
    categories = ServiceCategory.objects.order_by('name')
    return render(request, 'vibe/service_discovery.html', {'categories': categories})


def booking_configurator(request: HttpRequest) -> HttpResponse:
    return render(request, 'vibe/booking_configurator.html')


def provider_discovery(request: HttpRequest) -> HttpResponse:
    providers = (
        ServiceProvider.objects.filter(isVerified=True)
        .annotate(rating=Coalesce(Avg('bookings__review__rating'), Decimal('0.0')), reviews=Count('bookings__review'))
        .order_by('-rating', 'id')
    )
    return render(request, 'vibe/provider_discovery.html', {'providers': providers})


def checkout_summary(request: HttpRequest) -> HttpResponse:
    return render(request, 'vibe/checkout_summary.html')


@login_required
def customer_command_center(request: HttpRequest) -> HttpResponse:
    customer = Customer.objects.filter(user=request.user).first()
    now = timezone.now()
    bookings = []
    if customer:
        for booking in customer.bookings.select_related('category')[:10]:
            diff = booking.scheduledTime - now
            bookings.append(
                {
                    'id': booking.id,
                    'category': booking.category.name,
                    'status': booking.status,
                    'scheduled': booking.scheduledTime,
                    'can_cancel': diff >= timedelta(hours=48) and booking.status in (Booking.Status.PENDING, Booking.Status.ACCEPTED),
                }
            )

    return render(request, 'vibe/customer_command_center.html', {'bookings': bookings})


@login_required
def provider_workspace(request: HttpRequest) -> HttpResponse:
    provider = ServiceProvider.objects.filter(user=request.user).first()
    invites = []
    active_booking = None
    if provider:
        invites = Booking.objects.filter(service_provider=provider, status=Booking.Status.PENDING).select_related('category', 'customer')
        active_booking = (
            Booking.objects.filter(service_provider=provider, status__in=[Booking.Status.ACCEPTED, Booking.Status.STARTED])
            .select_related('category')
            .first()
        )

    return render(
        request,
        'vibe/provider_workspace.html',
        {
            'provider': provider,
            'invites': invites,
            'active_booking': active_booking,
        },
    )


def global_admin_dashboard(request: HttpRequest) -> HttpResponse:
    revenue = Booking.objects.filter(status=Booking.Status.COMPLETED).aggregate(
        total_revenue=Coalesce(Sum('category__basePrice'), Decimal('0.00')),
    )
    stats = ServiceProvider.objects.aggregate(active_cleaners=Count('id', filter=Q(isVerified=True)))
    pending_disputes = Review.objects.filter(comment__icontains='dispute').aggregate(total=Count('id'))

    context = {
        'total_revenue': revenue['total_revenue'],
        'active_cleaners': stats['active_cleaners'],
        'pending_disputes': pending_disputes['total'],
    }
    return render(request, 'vibe/admin_dashboard.html', context)


@login_required
def professional_kyc(request: HttpRequest) -> HttpResponse:
    provider, _ = ServiceProvider.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        provider.experienceInfo = request.POST.get('experienceInfo', provider.experienceInfo)
        if request.FILES.get('idProof'):
            provider.idProof = request.FILES['idProof']
        provider.save(update_fields=['experienceInfo', 'idProof'])
        return redirect('professional-kyc')

    return render(request, 'vibe/professional_kyc.html', {'provider': provider})


def feedback_success(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '').strip()
        if 1 <= rating <= 5:
            completed_booking = Booking.objects.filter(status=Booking.Status.COMPLETED).first()
            if completed_booking and not hasattr(completed_booking, 'review'):
                Review.objects.create(booking=completed_booking, rating=rating, comment=comment)
    return render(request, 'vibe/feedback_success.html')
