# Generated by Django 3.1.3 on 2021-02-22 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_auto_20210222_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainarticle',
            name='short_description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
