from django.db import models
from django.db.models import Avg, Count, Q, Value
from django.db.models.functions import Coalesce

from services.models import ServiceCategory
from users.models import Customer, ServiceProvider


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        STARTED = 'STARTED', 'Started'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    service_provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.SET_NULL,
        related_name='bookings',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='bookings')
    scheduledTime = models.DateTimeField()
    serviceAddress = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ('-scheduledTime',)

    def __str__(self) -> str:
        return f'Booking #{self.pk} - {self.category.name}'

    def find_best_provider(self, *, exclude_provider_ids: list[int] | None = None) -> ServiceProvider | None:
        active_statuses = [Booking.Status.PENDING, Booking.Status.ACCEPTED, Booking.Status.STARTED]
        excluded = exclude_provider_ids or []

        ranked_providers = (
            ServiceProvider.objects.filter(isVerified=True)
            .exclude(id__in=excluded)
            .annotate(
                average_rating=Coalesce(Avg('bookings__review__rating'), Value(0.0)),
                active_bookings=Count(
                    'bookings',
                    filter=Q(bookings__status__in=active_statuses),
                    distinct=True,
                ),
            )
            .order_by('-average_rating', 'active_bookings', 'id')
        )
        return ranked_providers.first()

    def assign_best_provider(self, *, exclude_provider_ids: list[int] | None = None) -> ServiceProvider | None:
        provider = self.find_best_provider(exclude_provider_ids=exclude_provider_ids)
        if provider is None:
            self.service_provider = None
            self.status = Booking.Status.PENDING
            self.save(update_fields=['service_provider', 'status'])
            return None

        self.service_provider = provider
        self.status = Booking.Status.ACCEPTED
        self.save(update_fields=['service_provider', 'status'])
        return provider

    def handle_provider_rejection(self, rejecting_provider: ServiceProvider) -> ServiceProvider | None:
        excluded_ids = [rejecting_provider.id]
        if self.service_provider_id:
            excluded_ids.append(self.service_provider_id)

        return self.assign_best_provider(exclude_provider_ids=excluded_ids)


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(rating__gte=1) & Q(rating__lte=5), name='review_rating_between_1_and_5'),
        ]

    def __str__(self) -> str:
        return f'Review for booking #{self.booking_id}'
