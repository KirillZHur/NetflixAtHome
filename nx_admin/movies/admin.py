import requests
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import Group
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from movies.contstant import TEMPLATE_ID
from movies.models import (
    CustomUser,
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork,
)
from movies.s3 import upload_video, upload_image
from django.utils.html import format_html
from django.conf import settings


def public_image_url(key: str) -> str:
    base = settings.MINIO_PUBLIC_BASE
    bucket = settings.MINIO_BUCKET_NAME
    return f"{base}/{bucket}/{key}"


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ("genre", "film_work")


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ("person", "film_work")


class FilmWorkAdminForm(forms.ModelForm):
    video_file = forms.FileField(
        label="Video file",
        required=True,
        help_text="Uploading movies to S3",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "mov", "avi", "mkv", "wmv", "webm"]
            )
        ], )
    preview_file = forms.FileField(
        label="Preview file",
        required=False,
        help_text="Uploading a movie image to S3",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "jpg", "png", "raw", "webp"]
            )
        ],
    )

    class Meta:
        model = FilmWork
        fields = "__all__"


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    form = FilmWorkAdminForm

    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)

    list_display = ("title", "type", "creation_date", "rating", "get_genres")
    list_filter = ("type", "creation_date", "genres")
    search_fields = ("title", "description", "id")

    exclude = ("video_s3_key", "preview_s3_key", "created_at", "updated_at")

    def get_genres(self, obj):
        return ",".join([genre.name for genre in obj.genres.all()])

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("genres")

    get_genres.short_description = _("genre")

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None

        video = form.cleaned_data.get("video_file")
        if video:
            obj.video_s3_key = upload_video(video)

        overview = form.cleaned_data.get("preview_file")
        if overview:
            obj.preview_s3_key = upload_image(overview)

        super().save_model(request, obj, form, change)

    readonly_fields = ("poster_preview",)
    fieldsets = (
        ("General", {
            "fields": ("title", "type", "description", "creation_date", "rating")
        }),
        ("Media", {
            "fields": ("preview_file", "poster_preview", "video_file")
        }),
    )

    def poster_preview(self, obj):
        if not obj or not getattr(obj, "preview_s3_key", None):
            return "—"
        url = public_image_url(obj.preview_s3_key)
        return format_html(
            '<div class="nx-preview"><img src="{}"></div>',
            url
        )

    poster_preview.short_description = "Saved preview file"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmWorkInline,)
    list_display = ("full_name",)
    search_fields = ("full_name",)


admin.site.unregister(Group)
