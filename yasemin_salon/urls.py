from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Ясемин — Управление'
admin.site.site_title = 'Ясемин Салон'
admin.site.index_title = 'Панель управления'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('salon.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
