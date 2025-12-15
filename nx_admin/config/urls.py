from config.settings import DEBUG
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from movies.views import check_static_settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("movies.api.urls")),
    path('check-static/', check_static_settings, name='check_static'),
]

if DEBUG:
    urlpatterns += debug_toolbar_urls()
