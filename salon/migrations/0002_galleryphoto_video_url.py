from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryphoto',
            name='video_url',
            field=models.URLField(blank=True, default='', verbose_name='Ссылка (Instagram/TikTok/YouTube)'),
        ),
    ]
