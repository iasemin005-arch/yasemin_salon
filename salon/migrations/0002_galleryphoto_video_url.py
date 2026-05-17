from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryphoto',
            name='video_url',
            field=models.URLField(blank=True, verbose_name='Ссылка на видео/фото (YouTube/Instagram)'),
        ),
        migrations.AlterField(
            model_name='galleryphoto',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='gallery/', verbose_name='Фото'),
        ),
    ]
