from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from spa import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('users/', include('users.urls')),
    path('', include('articles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

