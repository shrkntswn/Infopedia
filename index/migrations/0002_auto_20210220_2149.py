# Generated by Django 3.1.3 on 2021-02-20 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articles',
            old_name='articles',
            new_name='content',
        ),
    ]