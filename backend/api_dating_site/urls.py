from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [re_path(
    r'^backend_media/(?P<path>.*)$',
    serve,
    {'document_root': settings.MEDIA_ROOT, }),
]
