# Generated by Django 3.2.3 on 2024-10-25 09:12

from django.db import migrations, models
import shortener.models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmapped',
            name='original_url',
            field=models.CharField(max_length=256, verbose_name='Оригинальная ссылка'),
        ),
        migrations.AlterField(
            model_name='linkmapped',
            name='url_hash',
            field=models.CharField(default=shortener.models.generate_hash, max_length=15, unique=True, verbose_name='Короткая ссылка'),
        ),
    ]
