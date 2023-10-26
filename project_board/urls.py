from ckeditor_uploader.views import upload, browse
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import url

from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import never_cache


urlpatterns = [
                  path('ckeditor/upload/', upload, name='ckeditor_upload'),
                  path(r'ckeditor/browse/', never_cache(browse), name='ckeditor_browse'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('admin/', admin.site.urls),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('accounts/', include('accounts.urls')),
                  path('', include('posts.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


