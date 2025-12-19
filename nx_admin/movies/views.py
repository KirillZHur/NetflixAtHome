from django.shortcuts import render  # noqa: F401

# Create your views here.
from django.http import JsonResponse
from django.conf import settings
import os


def check_static_settings(request):
    """View для проверки настроек статических файлов"""

    # Проверяем существование папок
    static_dirs_exist = []
    for static_dir in settings.STATICFILES_DIRS:
        exists = os.path.exists(static_dir)
        static_dirs_exist.append({
            'path': str(static_dir),
            'exists': exists
        })

    # Проверяем STATIC_ROOT
    static_root_exists = os.path.exists(settings.STATIC_ROOT) if settings.STATIC_ROOT else False

    # Собираем информацию
    data = {
        'DEBUG': settings.DEBUG,
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_ROOT': str(settings.STATIC_ROOT),
        'STATIC_ROOT_exists': static_root_exists,
        'STATICFILES_DIRS': static_dirs_exist,
        'INSTALLED_APPS_has_staticfiles': 'django.contrib.staticfiles' in settings.INSTALLED_APPS,
    }

    return JsonResponse(data)
