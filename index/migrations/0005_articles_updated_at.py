# Generated by Django 3.1.3 on 2021-02-21 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_remove_articles_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
