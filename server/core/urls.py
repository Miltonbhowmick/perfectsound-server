from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from music.views import download_audio_file

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("api/v1/account/", include("account.urls", namespace="account")),
    path("api/v1/common/", include("common.urls", namespace="common")),
    path("api/v1/music/", include("music.urls", namespace="music")),
    path("api/v1/payment/", include("payment.urls", namespace="payment")),
    path("api/v1/order/", include("order.urls", namespace="order")),
    path("media/download/<path:path>/", download_audio_file, name="download_audio"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
