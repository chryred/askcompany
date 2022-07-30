from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django_pydenticon.views import image as pydenticon_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # re_path('')  모든 url에 매칭됨, 404관련된 처리시 유용
    path('identicon/image/<path:data>/', pydenticon_image, name="pydenticon_image"),
    path('instagram/', include('instagram.urls')),
    path('', login_required(RedirectView.as_view(pattern_name='instagram:index')), name='root'),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)