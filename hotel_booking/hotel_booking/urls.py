from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('all_bookings_and_registrations.urls')),  # Changed app name
]