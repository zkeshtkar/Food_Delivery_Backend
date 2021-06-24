from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', include('customers.urls')),
    path('accounts/', include('accounts.urls')),
    path('manager/', include('managers.urls')),
    path('about-us/', include('about_us.urls')),

]
