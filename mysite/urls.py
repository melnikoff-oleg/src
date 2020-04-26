from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), #Add Django site authentication urls (for login, logout, password management)
    path('', include('RAsite.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

