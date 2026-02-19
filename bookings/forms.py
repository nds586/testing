from django import forms
from django.utils import timezone

from bookings.models import Booking
from services.models import ServiceCategory


class ServiceCategorySelect(forms.Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_prices: dict[str, str] = {}

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        price = self.category_prices.get(str(value))
        if price:
            option['attrs']['data-base-price'] = price
        return option


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('category', 'scheduledTime', 'serviceAddress')
        widgets = {
            'category': ServiceCategorySelect(),
            'scheduledTime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'serviceAddress': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = ServiceCategory.objects.order_by('name')
        self.fields['category'].queryset = categories
        self.fields['scheduledTime'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
        category_widget = self.fields['category'].widget
        if isinstance(category_widget, ServiceCategorySelect):
            category_widget.category_prices = {str(category.pk): str(category.basePrice) for category in categories}
