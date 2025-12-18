from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="FilmWork",
            name="preview_s3_key",
            field=models.CharField(
                blank=True, max_length=512, null=True, verbose_name="preview s3 key"
            ),
        ),
        migrations.AddField(
            model_name="FilmWork",
            name="video_s3_key",
            field=models.CharField(
                blank=True, max_length=512, null=True, verbose_name="video s3 key"
            ),
        ),
    ]
