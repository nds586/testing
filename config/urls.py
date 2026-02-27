from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from bookings.views import create_booking, provider_invite_action
from services import views as vibe_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vibe_views.hero_landing, name='hero-landing'),
    path('services/', vibe_views.service_discovery, name='service-discovery'),
    path('booking/configurator/', vibe_views.booking_configurator, name='booking-configurator'),
    path('providers/results/', vibe_views.provider_discovery, name='provider-discovery'),
    path('checkout/', vibe_views.checkout_summary, name='checkout-summary'),
    path('customer/dashboard/', vibe_views.customer_command_center, name='customer-command-center'),
    path('provider/workspace/', vibe_views.provider_workspace, name='provider-workspace'),
    path('provider/invite/<int:booking_id>/<str:action>/', provider_invite_action, name='provider-invite-action'),
    path('global-admin/dashboard/', vibe_views.global_admin_dashboard, name='global-admin-dashboard'),
    path('provider/kyc/', vibe_views.professional_kyc, name='professional-kyc'),
    path('feedback/success/', vibe_views.feedback_success, name='feedback-success'),
    path('bookings/create/', create_booking, name='booking-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
