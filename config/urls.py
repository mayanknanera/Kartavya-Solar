from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Kartavya Solar Admin"
admin.site.site_title = "Kartavya Solar Admin"
admin.site.index_title = "Kartavya Solar Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),   # Google OAuth & allauth routes
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
